from md import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")


ds=ColumnDataSource(df)

p=figure(x_axis_type='datetime',height=100, width=500, sizing_mode = "scale_width", title="Motion Graph")
p.xaxis.axis_label="Date-Time"
p.yaxis.minor_tick_line_color=None #remove small tickers
p.ygrid[0].ticker.desired_num_ticks=1 #remove gridlines

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="blue",source=ds)

output_file("Graph1.html")
show(p)
