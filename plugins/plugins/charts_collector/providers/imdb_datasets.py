"""
IMDb Datasets 数据提供者
"""

import gzip
import io
import pandas as pd
from typing import Dict, List, Any
from .base import BaseProvider


class IMDBDatasetsProvider(BaseProvider):
    """IMDb Datasets 数据提供者"""
    
    def __init__(self):
        super().__init__()
        self.name = "imdb_datasets"
        self.description = "IMDb 数据集排行榜数据"
    
    async def fetch_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取IMDb数据集数据"""
        ratings_url = config.get("ratings_url", "https://datasets.imdbws.com/title.ratings.tsv.gz")
        basics_url = config.get("basics_url", "https://datasets.imdbws.com/title.basics.tsv.gz")
        join_basics = config.get("join_basics", True)
        min_votes = config.get("min_votes", 10000)
        top_n = config.get("top_n", 500)
        
        try:
            # 下载评分数据
            ratings_data = await self._http_get(ratings_url)
            ratings_df = self._parse_tsv_gz(ratings_data)
            
            # 过滤最低投票数
            ratings_df = ratings_df[ratings_df['numVotes'] >= min_votes]
            
            if join_basics:
                # 下载基本信息数据
                basics_data = await self._http_get(basics_url)
                basics_df = self._parse_tsv_gz(basics_data)
                
                # 合并数据
                merged_df = pd.merge(ratings_df, basics_df, on='tconst', how='inner')
                
                # 过滤电影类型
                merged_df = merged_df[merged_df['titleType'] == 'movie']
                
                # 按评分排序
                merged_df = merged_df.sort_values(['averageRating', 'numVotes'], ascending=[False, False])
                
                return self._parse_imdb_data(merged_df.head(top_n))
            else:
                # 仅使用评分数据
                ratings_df = ratings_df.sort_values(['averageRating', 'numVotes'], ascending=[False, False])
                return self._parse_ratings_data(ratings_df.head(top_n))
                
        except Exception as e:
            raise Exception(f"获取IMDb数据失败: {e}")
    
    def _parse_tsv_gz(self, gz_data: str) -> pd.DataFrame:
        """解析gzip压缩的TSV数据"""
        # 解压数据
        decompressed = gzip.decompress(gz_data.encode('utf-8'))
        
        # 使用pandas解析TSV
        return pd.read_csv(io.BytesIO(decompressed), sep='\t', low_memory=False)
    
    def _parse_imdb_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """解析IMDb完整数据"""
        results = []
        
        for i, (_, row) in enumerate(df.iterrows(), 1):
            result = {
                "source": "imdb_datasets",
                "region": "global",
                "chart_type": "ratings_top",
                "date_or_week": "latest",
                "rank": i,
                "title": row.get('primaryTitle', ''),
                "artist_or_show": row.get('genres', ''),
                "id_or_url": f"https://www.imdb.com/title/{row.get('tconst', '')}",
                "metrics": {
                    "avg_rating": float(row.get('averageRating', 0)),
                    "votes": int(row.get('numVotes', 0)),
                    "year": int(row.get('startYear', 0)) if pd.notna(row.get('startYear')) else 0
                }
            }
            results.append(result)
        
        return results
    
    def _parse_ratings_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """解析仅评分数据"""
        results = []
        
        for i, (_, row) in enumerate(df.iterrows(), 1):
            result = {
                "source": "imdb_datasets",
                "region": "global",
                "chart_type": "ratings_top",
                "date_or_week": "latest",
                "rank": i,
                "title": f"IMDb ID: {row.get('tconst', '')}",
                "artist_or_show": "",
                "id_or_url": f"https://www.imdb.com/title/{row.get('tconst', '')}",
                "metrics": {
                    "avg_rating": float(row.get('averageRating', 0)),
                    "votes": int(row.get('numVotes', 0))
                }
            }
            results.append(result)
        
        return results