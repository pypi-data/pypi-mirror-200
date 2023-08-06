"""
This is a light wrapper around polars with various methods and libraries monkey 
patched in.  It's all python specific so isn't really an improvement to the Rust
based underlying polars package.
"""

import polars as pl
import fsspec
import os

abfs = fsspec.filesystem('abfss', connection_string=os.environ['Synblob'])

def write_pq(self, REMOTE_PATH, **kwargs):
    with abfs.open(REMOTE_PATH, "wb") as file_pointer:
        self.write_parquet(file_pointer, **kwargs)
        
pl.DataFrame.write_pq=write_pq

def read_pq(REMOTE_PATH, **kwargs):
    with abfs.open(REMOTE_PATH, "rb") as file_pointer:
        return pl.read_parquet(file_pointer, **kwargs)
pl.read_pq=read_pq
try:
    import ipy_table as pt  
    def to_html(self):
        myL=[tuple(x for x in self.columns)]
        myL.extend(self.rows())
        return pt.IpyTable(myL)
    pl.DataFrame.to_html=to_html
except:
    pass


try:
    import plotly.express as px
    import plotly.io as pio
    pio.renderers.default='notebook_connected'
    try:
        px.set_mapbox_access_token(os.environ['MAPBOX_API_KEY'])
    except:
        pass
    @pl.api.register_dataframe_namespace("px")
    class mypx:
        def __init__(self, df: pl.DataFrame):
            self._df = df
        def bar(self, **kwargs):
            return px.bar(self._df.to_pandas(), **kwargs)
        def bar_polar(self, **kwargs):
            return px.bar_polar(self._df.to_pandas(), **kwargs)
        def box(self, **kwargs):
            return px.box(self._df.to_pandas(), **kwargs)
        def choropleth(self, **kwargs):
            return px.choropleth(self._df.to_pandas(), **kwargs)
        def choropleth_mapbox(self, **kwargs):
            return px.choropleth_mapbox(self._df.to_pandas(), **kwargs)
        def density_contour(self, **kwargs):
            return px.density_contour(self._df.to_pandas(), **kwargs)
        def density_heatmap(self, **kwargs):
            return px.density_heatmap(self._df.to_pandas(), **kwargs)
        def density_mapbox(self, **kwargs):
            return px.density_mapbox(self._df.to_pandas(), **kwargs)
        def ecdf(self, **kwargs):
            return px.ecdf(self._df.to_pandas(), **kwargs)
        def funnel(self, **kwargs):
            return px.funnel(self._df.to_pandas(), **kwargs)
        def funnel_area(self, **kwargs):
            return px.funnel_area(self._df.to_pandas(), **kwargs)
        def histogram(self, **kwargs):
            return px.histogram(self._df.to_pandas(), **kwargs)
        def icicle(self, **kwargs):
            return px.icicle(self._df.to_pandas(), **kwargs)
        def line(self, **kwargs):
            return px.line(self._df.to_pandas(), **kwargs)
        def line_3d(self, **kwargs):
            return px.line_3d(self._df.to_pandas(), **kwargs)
        def line_geo(self, **kwargs):
            return px.line_geo(self._df.to_pandas(), **kwargs)
        def line_mapbox(self, **kwargs):
            return px.line_mapbox(self._df.to_pandas(), **kwargs)
        def line_polar(self, **kwargs):
            return px.line_polar(self._df.to_pandas(), **kwargs)
        def line_ternary(self, **kwargs):
            return px.line_ternary(self._df.to_pandas(), **kwargs)
        def parallel_categories(self, **kwargs):
            return px.parallel_categories(self._df.to_pandas(), **kwargs)
        def parallel_coordinates(self, **kwargs):
            return px.parallel_coordinates(self._df.to_pandas(), **kwargs)
        def pie(self, **kwargs):
            return px.pie(self._df.to_pandas(), **kwargs)
        def scatter(self, **kwargs):
            return px.scatter(self._df.to_pandas(), **kwargs)
        def scatter_3d(self, **kwargs):
            return px.scatter_3d(self._df.to_pandas(), **kwargs)
        def scatter_geo(self, **kwargs):
            return px.scatter_geo(self._df.to_pandas(), **kwargs)
        def scatter_mapbox(self, **kwargs):
            return px.scatter_mapbox(self._df.to_pandas(), **kwargs)
        def scatter_matrix(self, **kwargs):
            return px.scatter_matrix(self._df.to_pandas(), **kwargs)
        def scatter_polar(self, **kwargs):
            return px.scatter_polar(self._df.to_pandas(), **kwargs)
        def scatter_ternary(self, **kwargs):
            return px.scatter_ternary(self._df.to_pandas(), **kwargs)
        def strip(self, **kwargs):
            return px.strip(self._df.to_pandas(), **kwargs)
        def sunburst(self, **kwargs):
            return px.sunburst(self._df.to_pandas(), **kwargs)
        def timeline(self, **kwargs):
            return px.timeline(self._df.to_pandas(), **kwargs)
        def treemap(self, **kwargs):
            return px.treemap(self._df.to_pandas(), **kwargs)
        def violin(self, **kwargs):
            return px.violin(self._df.to_pandas(), **kwargs)
except:
    pass

try:
    import statsmodels.api as sm
    @pl.api.register_dataframe_namespace("sm")
    class mysm:
        def __init__(self, df: pl.DataFrame):
            self._df = df
        def OLSsumm(self, yvar, xexprs, **kwargs):
            Y=self._df.select(yvar)
            X=self._df.select(xexprs)
            reg= sm.OLS(Y.to_numpy(), X.to_numpy()).fit(**kwargs)
            return reg.summary(xname=X.columns, yname=Y.columns[0])
except:
    pass