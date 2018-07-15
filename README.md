# RoomRenting
用Python爬取安居客房源信息，并用高德地图进行可视化

## 脚本介绍
- crawl_renting_info.py用来从相应租房网站上爬取租房信息，解析后存储到数据库中，与此同时将过程中的信息以日志的形式写入crawl_logger.log
- analyse_renting_info.py用来从数据库中读取出爬取的租房信息的地址，通过调用高德地址编码API转换为经纬度，去除转换错误以及地址本身有问题的数据，最后将有效的经纬度更新到原有的数据集合中，与此同时将过程中的信息以日志的形式写入analyse_logger.log
- export_renting_info.py用来将数据库中包含有效经纬度的租房信息以一定的格式导出到renting_info_mapdata.csv，以便之后调用高德的接口进行数据展示
- show_renting_info.py用来对数据库中的租房信息进行按照行政区域和地铁沿线进行统计和处理，以DataFrame的形式输出，便于读者查看
- search_renting_info.py用来与用户进行交互，通过对用户输入地址的经纬度转化，然后结合用户输入的其他租房条件，展示出距离用户输入地址一定范围的，满足用户条件的房源信息

## 效果展示
![info_in_mongodb](https://github.com/NightMarcher/RoomRenting/blob/master/image/info_in_mongodb.png?raw=true "info_in_mongodb")
![heat_map](https://github.com/NightMarcher/RoomRenting/blob/master/image/heat_map.png?raw=true "heat_map")
![district_map](https://github.com/NightMarcher/RoomRenting/blob/master/image/district_map.png?raw=true "district_map")
![line7](https://github.com/NightMarcher/RoomRenting/blob/master/image/line7.png?raw=true "line7")
![info_map_2](https://github.com/NightMarcher/RoomRenting/blob/master/image/info_map_2.png?raw=true "info_map_2")
![map_4_app](https://github.com/NightMarcher/RoomRenting/blob/master/image/map_4_app.png?raw=true "map_4_app")
![sum_4_district_info](https://github.com/NightMarcher/RoomRenting/blob/master/image/sum_4_district_info.png?raw=true "sum_4_district_info")
![sum_4_line_info](https://github.com/NightMarcher/RoomRenting/blob/master/image/sum_4_line_info.png?raw=true "sum_4_line_info")
