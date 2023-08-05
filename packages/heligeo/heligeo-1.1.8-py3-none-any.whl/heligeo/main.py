
import requests
import shapely
import numpy as np
import json
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import plotly.graph_objects as go


import dash

# from dash import dcc
# from dash import html
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
from numpy.lib.shape_base import column_stack
import dash_bootstrap_components as dbc

import shapefile
from pandas import DataFrame
import kml2geojson
from geo2kml import to_kml
import os
import ezdxf

# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input,Output




class heliRouteService:
    def route(apikey,lst,transport_mode):
		    payload = {'list':'{}'.format(lst),'apikey':'{}'.format(apikey),'transport-mode':'{}'.format(transport_mode)}
		    r = requests.post("https://nav.heliware.co.in/api/route/",data=payload)
		    return  r.json()
    def isochrone(apikey,lat,lon,transport_mode):
        payload = {'lat': lat, 'long':lon,'apikey':'{}'.format(apikey),'transport-mode':'{}'.format(transport_mode)}
        # "https://ai.heliware.co.in/api/ors_iso/"
        r = requests.get("https://ai.heliware.co.in/postgre/ors_iso/",params=payload)
        return  r.json()

class heliconverter:
    def shp_to_geojson(input_d,output_d):
        #output_directory = "D:/shape_file/online.geojson"
        #sf = shapefile.Reader(r"D:\shape_file\re\lines.shp")
        sf = shapefile.Reader(input_d)
        shapes = sf.shapes()
        geojson = shapes.__geo_interface__
        #with open("sample.json", "w") as outfile:
        with open(output_d, "w") as outfile:
            json.dump(geojson['geometries'], outfile)

    def kml_to_geojson(inputf,outputf):
        # srcDS = gdal.OpenEx(inputf)
        # ds = gdal.VectorTranslate(outputf, srcDS, format='GeoJSON')
        kml2geojson.main.convert(inputf,outputf)

    def geojson_to_kml(input_file_path,output_path):
        # input_file_path = "F:/heliware_project/Converter_Api/Converter/myshpfile2.geojson"
        # output_path = "D:/data5.kml"
        #subprocess.call("ogr2ogr -f KML {} {}".format(output_path,input_file_path),shell=True)
        kml_str = to_kml(json.loads(open(input_file_path).read()))
        with open(output_path, 'w') as f:
            f.write(kml_str)
            f.close()

    def obj_to_geojson(input_dir,output_dir):
        df_list = [] 
        f = open(input_dir, "r")
        for ln in f:
            if ln.startswith("v "):
                newln=ln.replace("v ","")
                df_list.append([float(newln.split(" ")[0]),float(newln.split(" ")[1]),float(newln.split(" ")[2])])
        f.close()
        fdata = {"data":"{}".format(df_list)}
        final_feature=requests.post('https://ai.heliware.co.in/api/object_to_geojson/',data=fdata)
        final_feature = final_feature.json()
        with open(output_dir, 'w', encoding='utf-8') as f:
            json.dump(final_feature,f)

    def geo_to_dxf(inputf,outputf):
        json_data = json.loads(open(inputf).read())

        dwg = ezdxf.new()
        modelspace = dwg.modelspace()
        for feature in json_data['features']:
            if feature['geometry']['type'] == "LineString":
                #print("geometry is line")
                for g in range(0,len(feature['geometry']['coordinates'])-1):
                    modelspace.add_line([feature['geometry']['coordinates'][g][0],feature['geometry']['coordinates'][g][1]],[feature['geometry']['coordinates'][g+1][0],feature['geometry']['coordinates'][g+1][1]])

            elif feature['geometry']['type'] == "MultiLineString":
                #print("geometry is multiline")
                for m in range(0,len(feature['geometry']['coordinates'])):
                    for g in range(0,len(feature['geometry']['coordinates'][m])-1):
                        modelspace.add_line([feature['geometry']['coordinates'][m][g][0],feature['geometry']['coordinates'][m][g][1]],[feature['geometry']['coordinates'][m][g+1][0],feature['geometry']['coordinates'][m][g+1][1]])

            elif feature['geometry']['type'] == "Polygon":
                #print("geometry is polygon")
                for g in range(0,len(feature['geometry']['coordinates'][0])-1):
                    modelspace.add_line([feature['geometry']['coordinates'][0][g][0],feature['geometry']['coordinates'][0][g][1]],[feature['geometry']['coordinates'][0][g+1][0],feature['geometry']['coordinates'][0][g+1][1]])

            elif feature['geometry']['type'] == "MultiPolygon":
                #print("geometry is multipolygon")
                for m in range(0,len(feature['geometry']['coordinates'])):
                    for g in range(0,len(feature['geometry']['coordinates'][m][0])-1):
                        modelspace.add_line([feature['geometry']['coordinates'][m][0][g][0],feature['geometry']['coordinates'][m][0][g][1]],[feature['geometry']['coordinates'][m][0][g+1][0],feature['geometry']['coordinates'][m][0][g+1][1]])

            elif feature['geometry']['type'] == "Point":
                #print("geometry is point")
                modelspace.add_point([feature['geometry']['coordinates'][0],feature['geometry']['coordinates'][1]])

            elif feature['geometry']['type'] == "MultiPoint":
                #print("geometry is multipoint")
                for g in range(0,len(feature['geometry']['coordinates'])):
                    modelspace.add_point([feature['geometry']['coordinates'][g][0],feature['geometry']['coordinates'][g][1]])

        dwg.saveas(outputf+".dxf")

class heliGeoprocessingService:
    
    def Union(apikey,newdata):
        # nd = "{}".format(newdata)
        # data = [{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "I1", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0], [77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [77.4029103817493, 28.36918941103731, 0.0]]]}}], "name": "I1"},{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "i2", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0.0], [77.40218550684746, 28.3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [77.40486731638147, 28.36831967535351, 0.0]]]}}], "name": "i2"}]
        payload = {"apikey":apikey,"data":"{}".format(newdata)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/union/",data=payload)
        return  r.json()
    def Intersection(apikey,newdata):
        # nd = "{}".format(newdata)
        # data = [{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "I1", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0], [77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [77.4029103817493, 28.36918941103731, 0.0]]]}}], "name": "I1"},{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "i2", "styleUrl": "#msn_ylw-pushpin"}, "geometry": {"type": "Polygon", "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0.0], [77.40218550684746, 28.3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [77.40486731638147, 28.36831967535351, 0.0]]]}}], "name": "i2"}]
        payload = {"apikey":apikey,"data":"{}".format(newdata)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/intersection/",data=payload)
        return  r.json()
    def PointBuffer(apikey,lst,area):
        payload = {"apikey":apikey,"area":area,"latlonglist":"{}".format(lst)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/bufferpolygon/",data=payload)
        return  r.json()

    def LineBuffer(apikey,lst,area):
        payload = {"apikey":apikey,"area":area,"latlonglist":"{}".format(lst)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/bufferline/",data=payload)
        return  r.json()
    def PointWithinPoly(apikey,pointdata,polydata):
        payload = {"apikey":apikey,"pointdata":"{}".format(pointdata),"polygondata":"{}".format(polydata)}
        r = requests.post("https://ai.heliware.co.in/api/geoprocessing/pointcheck/",data=payload)
        return r.json()
    def AliasLinestring(apikey,lsd,gap,quantity):
        payload = {"apikey":apikey,"lsd":"{}".format(lsd),"gap":"{}".format(gap),"quantity":"{}".format(quantity)}
        r = requests.post("https://ai.heliware.co.in/api/dls/",data=payload)
        return r.json()
    def CropGeo(apikey,bbdata,geodata):        
        payload = {"apikey":"{}".format(apikey),"bb":"{}".format(bbdata),"gd":"{}".format(geodata)}
        r = requests.post("https://ai.heliware.co.in/api/cg/",data=payload)
        return r.json()
    def PolyGrid(apikey,polygondata,gridsize):
        payload = {"apikey":"{}".format(apikey),"pd":"{}".format(polygondata),"gridsize":"{}".format(gridsize)}
        r = requests.post("https://ai.heliware.co.in/api/pg/",data=payload)
        return r.json()
    def PolyCenter(apikey,polygondata):
        payload = {"apikey":"{}".format(apikey),"pd":"{}".format(polygondata)}
        r = requests.post("https://ai.heliware.co.in/api/fpc/",data=payload)
        return r.json()
    def check_polygon_ls_within_poly(a,b,c):
        payload = {"apikey":a,"pp":"{}".format(b),"cp":"{}".format(c)}
        r = requests.post("https://ai.heliware.co.in/api/c/",data=payload)
        return r.json()
    def crop_polygon_using_linestring(apikey,pp,ls):
        payload = {"apikey":apikey,"pp":"{}".format(pp),"ls":"{}".format(ls)}
        r = requests.post("https://ai.heliware.co.in/api/cp/",data=payload)
        return r.json()

    ##### Mukul updates geoprocessing features #####
    def polygon_center(apikey,data):
        fdata = {"apikey":apikey,"data":"{}".format(data)}
        pc=requests.post('https://ai.heliware.co.in/api/polygon_center/',data=fdata)
        return pc.json()

    def distance_between_point(apikey,data):
        fdata = {"apikey":apikey,"data":"{}".format(data)}
        pc=requests.post('https://ai.heliware.co.in/api/Distance_between_two_points/',data=fdata)
        return pc.json()

    def boundingbox_geojson(apikey,data):
        fdata = {"apikey":apikey,"data":"{}".format(data)}
        pc=requests.post('https://ai.heliware.co.in/api/boundingbox_of_geojson/',data=fdata)
        return pc.json()

    def area_multipolygon(apikey,data):
        fdata = {"apikey":apikey,"data":"{}".format(data)}
        pc=requests.post('https://ai.heliware.co.in/api/multipolygon_area/',data=fdata)
        return pc.json()

    def linear_nearest_neighour(apikey,data,mark_point):
        fdata = {"apikey":apikey,"data":"{}".format(data),"point":"{}".format(mark_point)}
        pc=requests.post('https://ai.heliware.co.in/api/linear_nearest_neighour_point/',data=fdata)
        return pc.json()

    def point_within_polygon(apikey,data,scale):
        fdata = {"apikey":apikey,"data":"{}".format(data),"scale":"{}".format(scale)}
        pc=requests.post('https://ai.heliware.co.in/api/properties_based_multi_point_within_polygon/',data=fdata)
        return pc.json()

    def line_arc_from_point(apikey,data,measure):
        fdata = {"apikey":apikey,"data":"{}".format(data),"measure":"{}".format(measure)}
        pc=requests.post('https://ai.heliware.co.in/api/line_arc_by_point/',data=fdata)
        return pc.json()

    def nearest_point_along_line(apikey,data,url):
        fdata = {"apikey":apikey,"lsd":"{}".format(data),"url":url}
        pc=requests.post('https://ai.heliware.co.in/api/nearest_point_along_line/',data=fdata)
        return pc.json()
    ##### Mukul updates geoprocessing features end #####

# pp={"type":"FeatureCollection","name":"C:\\Users\\Administrator\\Desktop\\nandan\\polyogn2.geojson","features":[{"type":"Feature","properties":{"PERIMETER":"5.875km","ENCLOSED_AREA":"1.942sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.034290396156109,26.216521492685377],[73.021931558146761,26.213513116508437],[73.014575198080507,26.215434496713048],[73.016030076819263,26.224396491213852],[73.021912420893742,26.227479483772637],[73.026829206517533,26.224765669725592],[73.031471478784212,26.223914213532407],[73.029934010284904,26.218662651611364],[73.034290396156109,26.216521492685377]]]}}]}


# cp=[{"type":"FeatureCollection","name":"C:\\Users\\Administrator\\Desktop\\nandan\\poygon.geojson","features":[{"type":"Feature","properties":{"PERIMETER":"1.536km","ENCLOSED_AREA":"0.1559sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.017705095814193,26.214995615710134],[73.017653425231003,26.218664227116747],[73.020081942641013,26.219800979946964],[73.021270366054424,26.21938761528143],[73.021322036637613,26.21788916836887],[73.021270366054424,26.216545733205887],[73.020030272057824,26.215408980375667],[73.017705095814193,26.214995615710134]]]}},{"type":"Feature","properties":{"PERIMETER":"1.32km","ENCLOSED_AREA":"0.1249sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.022510460051024,26.21608069795716],[73.022355448301454,26.218147521284831],[73.022975495299761,26.219645968197391],[73.024370601045931,26.21969763878058],[73.025507353876151,26.219180932948664],[73.026024059708064,26.218560885950364],[73.026127400874444,26.217475803703337],[73.025920718541684,26.21670074495546],[73.024628953961894,26.216235709706737],[73.023957236380397,26.216132368540354],[73.022510460051024,26.21608069795716]]]}},{"type":"Feature","properties":{"PERIMETER":"1.441km","ENCLOSED_AREA":"0.1404sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.020340295556977,26.221867803274634],[73.020288624973787,26.225226391182098],[73.023078836466141,26.225484744098054],[73.023750554047623,26.223572932519961],[73.02323384821571,26.221971144441017],[73.022562130634213,26.221041073943567],[73.021322036637613,26.221041073943567],[73.020340295556977,26.221867803274634]]]}},{"type":"Feature","properties":{"PERIMETER":"1.197km","ENCLOSED_AREA":"0.0906sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.016516672400783,26.219542627031007],[73.015793284236111,26.222952885521661],[73.017963448730157,26.223469591353577],[73.018893519227603,26.222022815024211],[73.018893519227603,26.220989403360374],[73.018738507478034,26.220834391610801],[73.018170131062917,26.220421026945267],[73.016516672400783,26.219542627031007]]]}},{"type":"Feature","properties":{"PERIMETER":"1.477km","ENCLOSED_AREA":"0.1481sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.024938977461034,26.221712791525061],[73.025817377375304,26.224916367682948],[73.028245894785314,26.224554673600604],[73.028710930034038,26.222591191439317],[73.028194224202124,26.220421026945267],[73.026334083207217,26.220317685778884],[73.025765706792114,26.220679379861224],[73.024938977461034,26.221712791525061]]]}},{"type":"Feature","properties":{"PERIMETER":"1.685km","ENCLOSED_AREA":"0.1552sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.015689943069717,26.21726912137057],[73.013364766826086,26.220989403360374],[73.01243469632864,26.21938761528143],[73.012073002246296,26.217165780204187],[73.014294837323547,26.214375568711834],[73.01475987257227,26.214530580461407],[73.015483260736957,26.215253968626094],[73.015689943069717,26.21726912137057]]]}},{"type":"Feature","properties":{"PERIMETER":"1.268km","ENCLOSED_AREA":"0.0744sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.028607588867658,26.217734156619297],[73.030157706363411,26.21881923886632],[73.030571071028945,26.220162674029307],[73.032017847358304,26.22000766227973],[73.032069517941494,26.218870909449514],[73.030777753361704,26.217114109620994],[73.029641000531484,26.216907427288227],[73.027832530119781,26.21695909787142],[73.028607588867658,26.217734156619297]]]}},{"type":"Feature","properties":{"PERIMETER":"1.095km","ENCLOSED_AREA":"0.0652sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.018170131062917,26.226156461679548],[73.017808436980587,26.224658014766987],[73.014294837323547,26.224141308935071],[73.013933143241204,26.225226391182098],[73.01589662540249,26.226001449929974],[73.01724006056547,26.226208132262741],[73.018170131062917,26.226156461679548]]]}},{"type":"Feature","properties":{"PERIMETER":"1.173km","ENCLOSED_AREA":"0.0785sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.021063683721664,26.214220556962257],[73.02323384821571,26.21484060396056],[73.023698883464434,26.213807192296724],[73.0220454248023,26.21246375713374],[73.019875260308254,26.212412086550547],[73.019100201560377,26.21365218054715],[73.019255213309947,26.21401387462949],[73.01966857797548,26.214065545212684],[73.021063683721664,26.214220556962257]]]}},{"type":"Feature","properties":{"PERIMETER":"1.093km","ENCLOSED_AREA":"0.0727sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.01972024855867,26.226414814595508],[73.02096034255527,26.228895002588711],[73.023388859965294,26.228119943840834],[73.023698883464434,26.227344885092958],[73.022872154133367,26.226466485178697],[73.01972024855867,26.226414814595508],[73.01972024855867,26.226414814595508]]]}},{"type":"Feature","properties":{"PERIMETER":"1.492km","ENCLOSED_AREA":"0.1509sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.030054365197017,26.223314579604004],[73.030261047529791,26.226724838094658],[73.032172859107888,26.226879849844231],[73.033516294270868,26.224813026516564],[73.033877988353211,26.223624603103154],[73.032534553190217,26.222126156190594],[73.031242788610427,26.222126156190594],[73.030054365197017,26.223314579604004]]]}},{"type":"Feature","properties":{"PERIMETER":"805.89m","ENCLOSED_AREA":"0.02693sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.021425377804007,26.222797873772084],[73.021838742469541,26.224399661851027],[73.022820483550177,26.223572932519961],[73.022355448301454,26.222332838523361],[73.020954480414559,26.221350594973508],[73.021425377804007,26.222797873772084]]]}},{"type":"Feature","properties":{"PERIMETER":"750.59m","ENCLOSED_AREA":"0.02093sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.019100201560377,26.21701076845461],[73.019926930891444,26.218560885950364],[73.020288624973787,26.217217450787377],[73.019754233901565,26.215359906925666],[73.019100201560377,26.21701076845461]]]}},{"type":"Feature","properties":{"PERIMETER":"519.43m","ENCLOSED_AREA":"0.01502sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.026540765539977,26.222177826773784],[73.02690245962232,26.223314579604004],[73.027677518370197,26.222332838523361],[73.027470836037438,26.221506109192291],[73.026850789039131,26.221351097442717],[73.026540765539977,26.222177826773784]]]}},{"type":"Feature","properties":{"PERIMETER":"512.53m","ENCLOSED_AREA":"0.01126sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.0170850488159,26.221351097442717],[73.016689757766372,26.223166331600297],[73.017756766397383,26.222126156190594],[73.017911778146967,26.221557779775484],[73.017911778146967,26.221557779775484],[73.0170850488159,26.221351097442717]]]}},{"type":"Feature","properties":{"PERIMETER":"898.8m","ENCLOSED_AREA":"0.051sqkm"},"geometry":{"type":"Polygon","coordinates":[[[73.01377813149162,26.216442392039504],[73.01227195304817,26.218387906558579],[73.012402871822971,26.219192121889495],[73.01357144915886,26.21907759178228],[73.01509195766873,26.218225898012143],[73.01465653140589,26.21701076845461],[73.01377813149162,26.216442392039504]]]}}]}]
# c = heliGeoprocessingService.check_polygon_ls_within_poly("gftryetrfvdecgtr",pp,cp)
# print(c)



class heliVisualizationService:
    def hex_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',hexagon_quantity=10,zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>1:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = ff.create_hexbin_mapbox(data_frame=df, lat="lat", lon="long",nx_hexagon=hexagon_quantity, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
        
       
    def hex_map_from_csv(ak='',file_path='',lat_col_name='',long_col_name='',hover_properties='',basemap_style='light',hexagon_quantity=10,zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties,'lcn':lat_col_name,'longcn':long_col_name},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("KeyError!!")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = ff.create_hexbin_mapbox(data_frame=df, lat="lat", lon="long",nx_hexagon=hexagon_quantity, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        # fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        # fig.show()
                        return fig 

                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
          
    def scatter_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        # df1,df2,df3 = pd.DataFrame(lats),pd.DataFrame(lons),pd.DataFrame(name)
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.scatter_mapbox(df, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style)
                        fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")

    def scatter_map_from_csv(ak='',file_path='',lat_col_name='',long_col_name='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties,'lcn':lat_col_name,'longcn':long_col_name},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("KeyError!!")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.scatter_mapbox(df, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style)
                        # fig.update_layout(mapbox_style=basemap_style,margin=dict(b=0, t=0, l=0, r=0))
                        return fig

                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
          
    def line_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg2/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.line_mapbox(df, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties,zoom=zoom_level)
                        fig.update_layout(mapbox_style=basemap_style)
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
            


    def fill_geo_map_from_geojson(ak='',file_path='',color='red',basemap_style='carto-positron',legend=False,zoom_level=5):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    files ={'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg3/',files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        lats,lons= response.json()['lats'],response.json()['lons']
                        fig = go.Figure(go.Scattermapbox(
                        fill = "toself",
                        lon = lons, lat = lats,
                        marker = { 'size': 10, 'color': color }))

                        fig.update_layout(
                            mapbox = {
                                'style': basemap_style,
                                'zoom': zoom_level},
                            showlegend =legend)
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
            

    def density_map_from_geojson(ak='',file_path='',hover_properties='',basemap_style='light',zoom_level=10):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("Key error hover properties not exist in data")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.density_mapbox(df, lat='lat', lon='long', z=hover_properties, radius=20,zoom=zoom_level,mapbox_style=basemap_style)
                        return fig
                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")
            
           

    def density_map_from_csv(ak='',file_path='',lat_col_name='',long_col_name='',hover_properties='',basemap_style='light',zoom_level=16):
        if len(ak) > 1:
            res = requests.get("https://ai.heliware.co.in/api/get-api-key/")
            if res.json()['api-key'] == ak:
                px.set_mapbox_access_token(ak)
                if len(file_path) > 1:
                    nd,files = {'new_hp':hover_properties,'lcn':lat_col_name,'longcn':long_col_name},{'file': open(file_path, 'rb')}
                    response = requests.post('https://ai.heliware.co.in/api/glfg/',data=nd,files=files)
                    if "message" in response.json():
                        raise Exception("KeyError!!")
                    elif "lats" in response.json() and len(response.json()['lats'])>0:
                        df1,df2,df3 = pd.DataFrame(response.json()['lats']),pd.DataFrame(response.json()['lons']),pd.DataFrame(response.json()['name'])
                        df = pd.concat([df1,df2,df3],axis=1)
                        df.columns = ['lat','long',hover_properties]
                        fig = px.density_mapbox(df, lat='lat', lon='long', z=hover_properties, radius=10,zoom=0,mapbox_style=basemap_style)
                        return fig

                else:
                    raise Exception("please provide a valid file path")
            else:
                raise Exception("Api key is not valid!!!")
        else:
            raise Exception("Please provide a valid api key!!!!")





class heliVisualizationWithFilteration:
    
    def visualization_from_geojson(filepath,hover_properties,map_style='dark'):
        app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
        px.set_mapbox_access_token("pk.eyJ1IjoiYmFwdXAiLCJhIjoiY2t0M3oxd2k0MHo0NzJwczJldXljNmpndyJ9.D95x6e6ya2VdFhvnhOViXA")
        comb={'botton_bg_color':'#444544','text_color1':'#DBE1DE','dropdown_color':'#8C8C8C','botton_on_map_color':'#333333','h_color':'#BEB9FA'}
        logo_image = 'https://raw.githubusercontent.com/mukulsharma97/Heliware_Visualization/main/assets/logo_transparent01.png'
        try:
            files = {'file': open(filepath, 'rb')}
            response = requests.post('https://ai.heliware.co.in/api/dlgf/',files=files)
        except Exception as e:
            print(e)
        if response.status_code == 200:
            if "message" in response.json():
                raise Exception("we accept only .geojson file")
            fl_df,lng_df,lat_df = pd.DataFrame(response.json()['fl']),pd.DataFrame(response.json()['long']),pd.DataFrame(response.json()['lat'])
            data = fl_df.join([lng_df,lat_df])
            columns_name = [col for col in data.columns if col!='lat' if col!='long']
            if columns_name[0] == 'Unnamed: 0':
                columns_name.pop(0)
            if len(columns_name) > 10:
                columns_name = columns_name[0:10]
            if hover_properties not in columns_name:
                raise Exception("not in data frame")
           
            app.layout = html.Div(style={'background-image':'url(https://raw.githubusercontent.com/mukulsharma97/Heliware_Visualization/main/assets/wallpaper.png)',
                'background-size':'cover','position':'relative','width':'100%','height':'100vh',
                'overflow-x':'hidden'},children=[
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content'),
            ])
            ## map for index page
            index_page = html.Div([
                html.Img(src=logo_image,style={'width':'200px','height':'60px'}),
                html.H1("Welcome to heli visualization dashboard!!!!",style={"text-align":"center","margin-top":"100px","color":comb['h_color'],"text-shadow": "2px 2px 2px gray,2px 2px 2px gray","font-size":"60px",'font-family':'TimesNewRoman','font-weight': '700'}),
                html.H2("Please select a Layer",style={"text-align":"center","color":comb['text_color1'],"margin-bottom":"60px","text-shadow": "1px 1px 1px gray,2px 2px 1px gray","padding": "40px 40px","font-size":"30px",'font-family':'TimesNewRoman','font-weight': '700'}),
                html.Div([dcc.Link('ScatterMap', href='/ScatterMap',style={"margin-top":"100px","background-color": comb['botton_bg_color'],"color": comb['text_color1'],"padding": "30px 40px","text-align": "center","text-decoration": "none","font-size":"40px"}),
                dcc.Link('DensityMap', href='/DensityMap',style={"margin-left":"5%","margin-top":"100px","background-color": comb['botton_bg_color'],"color": comb['text_color1'],"padding": "30px 40px","text-align": "center","text-decoration": "none","display": "inline","font-size":"40px"}),
                dcc.Link('HexagonMap', href='/HexagonMap',style={"margin-left":"5%","margin-top":"100px","background-color": comb['botton_bg_color'],"color": comb['text_color1'],"padding": "30px 40px","text-align": "center","text-decoration": "none","display": "inline","font-size":"40px"}),
                dcc.Link('LineMap', href='/lineMap',style={"margin-left":"5%","margin-top":"100px","background-color": comb['botton_bg_color'],"color": comb['text_color1'],"padding": "30px 40px","text-align": "center","text-decoration": "none","display": "inline","font-size":"40px"}),],style={'text-align':'center'})
                # dcc.Graph(figure=base_fig)
            ],style={'margin-bottom':'0%'})
           
            scatter_fig = px.scatter_mapbox(data, lat='lat', lon='long',labels={"color":hover_properties},color=hover_properties)
            scatter_fig.update_layout(mapbox_style=map_style,margin=dict(b=0, t=0, l=0, r=0),template='plotly_dark',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
            scatter_map_children_list,scatter_map_input_list = [],[]
            scatter_map_children_list.append(dbc.Row(html.H4("Filtration",style={"margin-top":"5%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            for i in columns_name:
                scatter_map_children_list.append(html.Div(children=i, className="menu-title",
                                style={"text-align":"center","color":comb['text_color1'],"margin-top":"5px","padding": "0px 20px",'font-weight': '400'}),)
                scatter_map_children_list.append(dcc.Dropdown(
                                id="{}-filter".format(i),
                                options=[
                                    {"label": region, "value": region}
                                    for region in data[i].unique()
                                    # for region in sorted(data[i].unique())
                                ],
                                value=[b for b in data[i].unique()],
                                clearable=False,
                                className="dropdown",
                                style={'background-color':comb['dropdown_color'],'border':'0px'}
                            ),
                )
                scatter_map_input_list.append(Input("{}-filter".format(i),"value"))
            scatter_map_children_list.append(dbc.Row(html.H4("More Map Options",style={"margin-top":"10%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            scatter_map_children_list.append(dbc.Row([dbc.Col(dcc.Link('DensityMap', href='/DensityMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('HexagonMap', href='/HexagonMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('LineMap', href='/lineMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0})],justify="around",style={'margin-top':'5%','margin-bottom':'10%'}))
            scatter_map_layout = html.Div([dbc.Row([dbc.Col(html.Img(src=logo_image,style={'width':'120px','height':'36px'})),
                dbc.Col(html.H3("Scatter Map",style={"margin-top":"2%","color":comb['h_color'],"font-size":"40px",'font-family':'TimesNewRoman','font-weight': '700'}))],justify="start"),
                dbc.Row([dbc.Col(children=scatter_map_children_list,width={'size':3,'offset':0.5},style={'background-color':comb['botton_bg_color']}),
                dbc.Col(dcc.Graph(id='scatter-graph',figure=scatter_fig,config={'displayModeBar': False},style={'height':'90vh'}),width={'size':8,'offset':0})],justify="center"),
            ])
            @app.callback(Output("scatter-graph", "figure"),scatter_map_input_list)
            def scattermap_update(*args,**kwargs):
                if None not in args:
                    if len(args) ==2:
                        if type(args[0])==list and type(args[1])==list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            
                            nd = data[((data[columns_name[0]] == args[0])&(data[columns_name[1]] == args[1]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    elif len(args) ==1:
                        if type(args[0])==list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[data[columns_name[0]] == args[0]]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    if len(args) ==3:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    if len(args) ==4:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    if len(args) ==5:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    if len(args) ==6:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        
                    if len(args) ==7:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    if len(args) ==8:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    if len(args) ==9:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8]))]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                    if len(args) ==10:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list and type(args[9]) == list:
                            fig = px.scatter_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) & ((data[columns_name[9]] == args[9])) ]
                            fig = px.scatter_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            return fig
            
            density_fig = px.density_mapbox(data, lat='lat', lon='long',z=hover_properties, radius=10,zoom=10)
            density_fig.update_layout(mapbox_style=map_style,margin=dict(b=0, t=0, l=0, r=0),template='plotly_dark',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
            density_map_children_list,density_map_input_list = [],[]
            density_map_children_list.append(dbc.Row(html.H4("Filtration",style={"margin-top":"5%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            for i in columns_name:
                density_map_children_list.append(html.Div(children=i, className="menu-title",
                                style={"text-align":"center","color":comb['text_color1'],"margin-top":"5px","padding": "0px 20px",'font-weight': '400'}),)
                density_map_children_list.append(dcc.Dropdown(
                                id="{}-filter".format(i),
                                options=[
                                    {"label": region, "value": region}
                                    for region in data[i].unique()
                                    # for region in sorted(data[i].unique())
                                ],
                                value=[b for b in data[i].unique()],
                                clearable=False,
                                className="dropdown",
                                style={'background-color':comb['dropdown_color'],'border':'0px'}
                            ),
                )
                density_map_input_list.append(Input("{}-filter".format(i),"value"))
            density_map_children_list.append(dbc.Row(html.H4("More Map Options",style={"margin-top":"10%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            density_map_children_list.append(dbc.Row([dbc.Col(dcc.Link('ScatterMap', href='/ScatterMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('HexagonMap', href='/HexagonMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('LineMap', href='/lineMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0})],justify="around",style={'margin-top':'5%','margin-bottom':'10%'}))
            density_map_layout = html.Div([dbc.Row([dbc.Col(html.Img(src=logo_image,style={'width':'120px','height':'36px'})),
                dbc.Col(html.H3("Density Map",style={"margin-top":"2%","color":comb['h_color'],"font-size":"40px",'font-family':'TimesNewRoman','font-weight': '700'}))],justify="start"),
                dbc.Row([dbc.Col(children=density_map_children_list,width={'size':3,'offset':0.5},style={'background-color':comb['botton_bg_color']}),
                dbc.Col(dcc.Graph(id='density-graph',figure=density_fig,config={'displayModeBar': False},style={'height':'90vh'}),width={'size':8,'offset':0})],justify="center"),
            ])
            @app.callback(Output("density-graph", "figure"),density_map_input_list)
            def densitymap_update(*args,**kwargs):
                print(len(args))
                if None not in args:
                    if len(args) ==2:
                        if type(args[0])==list and type(args[1])==list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            
                            nd = data[((data[columns_name[0]] == args[0])&(data[columns_name[1]] == args[1]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==1:
                        if type(args[0])==list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[data[columns_name[0]] == args[0]]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==3:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==4:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==5:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==6:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        
                    if len(args) ==7:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==8:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==9:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8]))]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==10:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list and type(args[9]) == list:
                            fig = px.density_mapbox(data, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) & ((data[columns_name[9]] == args[9])) ]
                            fig = px.density_mapbox(nd, lat='lat', lon='long', z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                          
            
            line_fig = px.line_mapbox(data, lat='lat', lon='long',labels={"color":hover_properties},color=hover_properties)
            line_fig.update_layout(mapbox_style=map_style,margin=dict(b=0, t=0, l=0, r=0),template='plotly_dark',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
            line_map_children_list,line_map_input_list = [],[]
            line_map_children_list.append(dbc.Row(html.H4("Filtration",style={"margin-top":"5%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            for i in columns_name:
                line_map_children_list.append(html.Div(children=i, className="menu-title",
                                style={"text-align":"center","color":comb['text_color1'],"margin-top":"5px","padding": "0px 20px",'font-weight': '400'}),)
                line_map_children_list.append(dcc.Dropdown(
                                id="{}-filter".format(i),
                                options=[
                                    {"label": region, "value": region}
                                    for region in data[i].unique()
                                    # for region in sorted(data[i].unique())
                                ],
                                value=[b for b in data[i].unique()],
                                clearable=False,
                                className="dropdown",
                                style={'background-color':comb['dropdown_color'],'border':'0px'}
                            ),
                )
                line_map_input_list.append(Input("{}-filter".format(i),"value"))
            line_map_children_list.append(dbc.Row(html.H4("More Map Options",style={"margin-top":"10%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            line_map_children_list.append(dbc.Row([dbc.Col(dcc.Link('ScatterMap', href='/ScatterMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 15px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('DensityMap', href='/DensityMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 15px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('HexagonMap', href='/HexagonMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 15px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0})],justify="around",style={'margin-top':'5%','margin-bottom':'10%'}))
            line_map_layout = html.Div([dbc.Row([dbc.Col(html.Img(src=logo_image,style={'width':'120px','height':'36px'})),
                dbc.Col(html.H3("Line Map",style={"margin-top":"2%","color":comb['h_color'],"font-size":"40px",'font-family':'TimesNewRoman','font-weight': '700'}))],justify="start"),
                dbc.Row([dbc.Col(children=line_map_children_list,width={'size':3,'offset':0.5},style={'background-color':comb['botton_bg_color']}),
                dbc.Col(dcc.Graph(id='line-graph',figure=line_fig,config={'displayModeBar': False},style={'height':'90vh'}),width={'size':8,'offset':0})],justify="center"),
            ])
            @app.callback(Output("line-graph", "figure"),line_map_input_list)
            def linemap_update(*args,**kwargs):
                # print(len(args))
                if None not in args:
                    if len(args) ==2:
                        if type(args[0])==list and type(args[1])==list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            
                            nd = data[((data[columns_name[0]] == args[0])&(data[columns_name[1]] == args[1]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==1:
                        if type(args[0])==list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[data[columns_name[0]] == args[0]]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==3:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==4:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==5:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==6:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        
                    if len(args) ==7:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==8:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==9:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8]))]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    if len(args) ==10:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list and type(args[9]) == list:
                            fig = px.line_mapbox(data, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) &((data[columns_name[3]] == args[3])) &((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) &((data[columns_name[6]] == args[6])) &((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) & ((data[columns_name[9]] == args[9])) ]
                            fig = px.line_mapbox(nd, lat="lat", lon="long",labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
            
            column_names = ['lat','lons','data']
            df = pd.DataFrame(columns = column_names)
            hexa_fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
            # hexa_fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=30, opacity=1,labels={"color":columns_name[0]},color=columns_name[0],zoom=8)
            # hexa_fig.update_layout(mapbox_style="light")
            hexa_fig.update_layout(mapbox_style="light",margin=dict(b=0, t=0, l=0, r=0))
            hexa_map_children_list,hexa_map_input_list = [],[]
            hexa_map_children_list.append(dbc.Row(html.H4("Filtration",style={"margin-top":"5%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            for i in columns_name:
                hexa_map_children_list.append(html.Div(children=i, className="menu-title",
                                style={"text-align":"center","color":comb['text_color1'],"margin-top":"5px","padding": "0px 20px",'font-weight': '400'}),)
                hexa_map_children_list.append(dcc.Dropdown(
                                id="{}-filter".format(i),
                                options=[
                                    {"label": region, "value": region}
                                    for region in data[i].unique()
                                    # for region in sorted(data[i].unique())
                                ],
                                value=[b for b in data[i].unique()],
                                clearable=False,
                                className="dropdown",
                                style={'background-color':comb['dropdown_color'],'border':'0px'}
                            ),
                )
                hexa_map_input_list.append(Input("{}-filter".format(i),"value"))
            hexa_map_children_list.append(dbc.Row(html.H4("More Map Options",style={"margin-top":"10%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            hexa_map_children_list.append(dbc.Row([dbc.Col(dcc.Link('LineMap', href='/lineMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('DensityMap', href='/DensityMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('ScatterMap', href='/ScatterMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0})],justify="around",style={'margin-top':'5%','margin-bottom':'10%'}))
            hexagon_map_layout = html.Div([dbc.Row([dbc.Col(html.Img(src=logo_image,style={'width':'120px','height':'36px'})),
                dbc.Col(html.H3("Hexagon Map",style={"margin-top":"2%","color":comb['h_color'],"font-size":"40px",'font-family':'TimesNewRoman','font-weight': '700'}))],justify="start"),
                dbc.Row([dbc.Col(children=hexa_map_children_list,width={'size':3,'offset':0.5},style={'background-color':comb['botton_bg_color']}),
                dbc.Col(dcc.Graph(id='hexa-graph',figure=hexa_fig,config={'displayModeBar': False},style={'height':'90vh'}),width={'size':8,'offset':0})],justify="center"),
            ])
            @app.callback(Output("hexa-graph", "figure"),hexa_map_input_list)
            def hexamap_update(*args,**kwargs):
                # print(len(args))
                if None not in args:
                    if len(args) ==2:
                        if type(args[0])==list and type(args[1])==list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1]))]
                            if len(nd)>0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                            
                    elif len(args) ==1:
                        if type(args[0])==list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[data[columns_name[0]] == args[0]]
                            if len(nd) > 0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==3:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2]))]
                            if len(nd) > 0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==4:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3]))]
                            if len(nd) > 0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==5:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4]))]
                            if len(nd) > 0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                        
                    elif len(args) ==6:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5]))]
                            if len(nd)>0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                            
                    
                    elif len(args) ==7:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else: 
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6]))]
                            if len(nd)>0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==8:
                       
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list:
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7]))]
                            if len(nd) > 0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==9:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list :
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8]))]
                            if len(nd) > 0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==10:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list and type(args[9]) == list :
                            fig = ff.create_hexbin_mapbox(data_frame=data, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) & ((data[columns_name[9]] == args[9]))]
                            if len(nd) > 0:
                                fig = ff.create_hexbin_mapbox(data_frame=nd, lat="lat", lon="long",nx_hexagon=10, opacity=0.9,labels={"color": hover_properties},color=hover_properties)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                            
            
            
            @app.callback(dash.dependencies.Output('page-content', 'children'),[dash.dependencies.Input('url', 'pathname')])
            def display_page(pathname):
                if pathname == '/ScatterMap':
                    return scatter_map_layout
                elif pathname == '/DensityMap':
                    return density_map_layout
                elif pathname == '/HexagonMap':
                    return hexagon_map_layout
                elif pathname == '/lineMap':
                    return line_map_layout
                else:
                    return index_page
            app.run_server(debug=False)
            #############################################hexagon map end ################
        else:
            raise Exception("status code {}".format(response.status_code))
    def visualization_from_csv(filepath,lcn,longcn,hover_properties,map_style='dark'):
        app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
        comb={'botton_bg_color':'#444544','text_color1':'#DBE1DE','dropdown_color':'#8C8C8C','botton_on_map_color':'#333333','h_color':'#0FC409'}
        logo_image = 'https://raw.githubusercontent.com/mukulsharma97/Heliware_Visualization/main/assets/logo_transparent01.png'
        px.set_mapbox_access_token("pk.eyJ1IjoiYmFwdXAiLCJhIjoiY2t0M3oxd2k0MHo0NzJwczJldXljNmpndyJ9.D95x6e6ya2VdFhvnhOViXA")
        if filepath.split(".")[-1] == 'csv':
            data = pd.read_csv(filepath)
            columns_name = [col for col in data.columns if col!=lcn if col!=longcn]
            if columns_name[0] == 'Unnamed: 0':
                columns_name.pop(0)
            if len(columns_name) > 10:
                columns_name = columns_name[0:10]
            if hover_properties not in columns_name:
                raise Exception("{} not in data set".format(hover_properties))
            ########################################### dash app home page ##################
            app.layout = html.Div(style={'background-image':'url(https://raw.githubusercontent.com/mukulsharma97/Heliware_Visualization/main/assets/wallpaper.png)',
                'background-size':'cover','position':'relative','width':'100%','height':'100vh',
                'overflow-x':'hidden'},children=[
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content')
            ])
            
            index_page = html.Div([
                html.Img(src=logo_image,style={'width':'200px','height':'60px'}),
                html.H1("Welcome to heli visualization dashboard!!!!",style={"text-align":"center","margin-top":"100px","color":comb['h_color'],"text-shadow": "2px 2px 2px gray,2px 2px 2px gray","font-size":"60px",'font-family':'TimesNewRoman','font-weight': '700'}),
                html.H2("Please select a Layer",style={"text-align":"center","color":comb['text_color1'],"margin-bottom":"60px","text-shadow": "1px 1px 1px gray,2px 2px 1px gray","padding": "40px 40px","font-size":"30px",'font-family':'TimesNewRoman','font-weight': '700'}),
                html.Div([dcc.Link('ScatterMap', href='/ScatterMap',style={"margin-top":"100px","background-color": comb['botton_bg_color'],"color": comb['text_color1'],"padding": "30px 40px","text-align": "center","text-decoration": "none","font-size":"40px"}),
                dcc.Link('DensityMap', href='/DensityMap',style={"margin-left":"5%","margin-top":"100px","background-color": comb['botton_bg_color'],"color": comb['text_color1'],"padding": "30px 40px","text-align": "center","text-decoration": "none","display": "inline","font-size":"40px"}),
                dcc.Link('HexagonMap', href='/HexagonMap',style={"margin-left":"5%","margin-top":"100px","background-color": comb['botton_bg_color'],"color": comb['text_color1'],"padding": "30px 40px","text-align": "center","text-decoration": "none","display": "inline","font-size":"40px"}),],style={'text-align':'center'})
            ],style={'margin-bottom':'0%'})

            scatter_fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
            scatter_fig.update_layout(mapbox_style=map_style)
            scatter_fig.update_layout(margin=dict(b=0, t=0, l=0, r=0),template='plotly_dark',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
            scatter_map_children_list,scatter_map_input_list = [],[]
            scatter_map_children_list.append(dbc.Row(html.H4("Filtration",style={"margin-top":"5%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            for i in columns_name:
                scatter_map_children_list.append(html.Div(children=i, className="menu-title",
                    style={"text-align":"center","color":comb['text_color1'],"margin-top":"5px","padding": "0px 20px",'font-weight': '400'}))
                scatter_map_children_list.append(dcc.Dropdown(
                                id="{}-filter".format(i),
                                options=[
                                    {"label": region, "value": region}
                                    for region in data[i].unique()
                                    # for region in sorted(data[i].unique())
                                ],
                                value=[b for b in data[i].unique()],
                                # value=[b for b in sorted(data[i].unique())],
                                # value="Albany",
                                clearable=False,
                                className="dropdown",
                                style={'background-color':comb['dropdown_color'],'border':'0px'}
                            ),
                    )
                scatter_map_input_list.append(Input("{}-filter".format(i),"value"))
            scatter_map_children_list.append(dbc.Row(html.H4("More Map Options",style={"margin-top":"10%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            scatter_map_children_list.append(dbc.Row([dbc.Col(dcc.Link('DensityMap', href='/DensityMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('HexagonMap', href='/HexagonMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0})],justify="around",style={'margin-top':'5%','margin-bottom':'10%'}))
            scatter_map_layout = html.Div([dbc.Row([dbc.Col(html.Img(src=logo_image,style={'width':'120px','height':'36px'})),
                dbc.Col(html.H3("Scatter Map",style={"margin-top":"2%","color":comb['h_color'],"font-size":"40px",'font-family':'TimesNewRoman','font-weight': '700'}))],justify="start"),
                dbc.Row([dbc.Col(children=scatter_map_children_list,width={'size':3,'offset':0.5},style={'background-color':comb['botton_bg_color']}),
                dbc.Col(dcc.Graph(id='scatter-graph',figure=scatter_fig,config={'displayModeBar': False},style={'height':'90vh'}),width={'size':8,'offset':0})],justify="center"),
            ])
            @app.callback(Output("scatter-graph", "figure"),scatter_map_input_list)
            def scattermap_update(*args,**kwargs):
                
                if None not in args:
                    if len(args) ==2:
                        if type(args[0])==list and type(args[1])==list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1]))]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==1:
                        if type(args[0])==list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[data[columns_name[0]] == args[0]]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==3:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            # nd = data[((data[columns_name[0]] == args[0])|(data[columns_name[1]] == args[0]) | (data[columns_name[2]] == args[0]))&((data[columns_name[0]] == args[1]) |(data[columns_name[1]] == args[1]) | (data[columns_name[2]] == args[1]))]
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2]))]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==4:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            # nd = data[((data[columns_name[0]] == args[0])|(data[columns_name[1]] == args[0]) | (data[columns_name[3]] == args[0]) | (data[columns_name[3]] == args[0]))&((data[columns_name[0]] == args[1]) |(data[columns_name[1]] == args[1]) | (data[columns_name[2]] == args[1]) | (data[columns_name[3]] == args[1]))]
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3]))]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==5:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4]))]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==6:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5]))]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==7:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6]))]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==8:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7]))]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==9:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) ]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    
                    elif len(args) ==10:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list and type(args[9]) == list:
                            fig = px.scatter_mapbox(data, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) & ((data[columns_name[9]] == args[9])) ]
                            fig = px.scatter_mapbox(nd, lat=lcn, lon=longcn ,labels={"color":hover_properties},color=hover_properties)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    
          
            density_fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
            density_fig.update_layout(mapbox_style=map_style)
            density_fig.update_layout(mapbox_style=map_style,margin=dict(b=0, t=0, l=0, r=0),template='plotly_dark',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
            density_map_children_list,density_map_input_list = [],[]
            density_map_children_list.append(dbc.Row(html.H4("Filtration",style={"margin-top":"5%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            for i in columns_name:
                density_map_children_list.append(html.Div(children=i, className="menu-title",
                    style={"text-align":"center","color":comb['text_color1'],"margin-top":"5px","padding": "0px 20px",'font-weight': '400'}))
                density_map_children_list.append(dcc.Dropdown(
                                id="{}-filter".format(i),
                                options=[
                                    {"label": region, "value": region}
                                    for region in data[i].unique()
                                    # for region in sorted(data[i].unique())
                                ],
                                value=[b for b in data[i].unique()],
                                # value=[b for b in sorted(data[i].unique())],
                                # value="Albany",
                                clearable=False,
                                className="dropdown",
                                style={'background-color':comb['dropdown_color'],'border':'0px'}
                            ),
                    )
                density_map_input_list.append(Input("{}-filter".format(i),"value"))
            density_map_children_list.append(dbc.Row(html.H4("More Map Options",style={"margin-top":"10%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            density_map_children_list.append(dbc.Row([dbc.Col(dcc.Link('ScatterMap', href='/ScatterMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('HexagonMap', href='/HexagonMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0})],justify="around",style={'margin-top':'5%','margin-bottom':'10%'}))
            density_map_layout = html.Div([dbc.Row([dbc.Col(html.Img(src=logo_image,style={'width':'120px','height':'36px'})),
                dbc.Col(html.H3("Density Map",style={"margin-top":"2%","color":comb['h_color'],"font-size":"40px",'font-family':'TimesNewRoman','font-weight': '700'}))],justify="start"),
                dbc.Row([dbc.Col(children=density_map_children_list,width={'size':3,'offset':0.5},style={'background-color':comb['botton_bg_color']}),
                dbc.Col(dcc.Graph(id='density-graph',figure=density_fig,config={'displayModeBar': False},style={'height':'90vh'}),width={'size':8,'offset':0})],justify="center"),
            ])
            @app.callback(Output("density-graph", "figure"),density_map_input_list)
            def densitymap_update(*args,**kwargs):
                if None not in args:
                    if len(args) ==2:
                        if type(args[0])==list and type(args[1])==list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1]))]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==1:
                        if type(args[0])==list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[data[columns_name[0]] == args[0]]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==3:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            # nd = data[((data[columns_name[0]] == args[0])|(data[columns_name[1]] == args[0]) | (data[columns_name[2]] == args[0]))&((data[columns_name[0]] == args[1]) |(data[columns_name[1]] == args[1]) | (data[columns_name[2]] == args[1]))]
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2]))]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==4:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            # nd = data[((data[columns_name[0]] == args[0])|(data[columns_name[1]] == args[0]) | (data[columns_name[3]] == args[0]) | (data[columns_name[3]] == args[0]))&((data[columns_name[0]] == args[1]) |(data[columns_name[1]] == args[1]) | (data[columns_name[2]] == args[1]) | (data[columns_name[3]] == args[1]))]
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3]))]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==5:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4]))]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==6:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5]))]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==7:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6]))]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==8:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7]))]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    elif len(args) ==9:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) ]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                    
                    elif len(args) ==10:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list and type(args[9]) == list:
                            fig = px.density_mapbox(data, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) & ((data[columns_name[9]] == args[9])) ]
                            fig = px.density_mapbox(nd, lat=lcn, lon=longcn, z=hover_properties, radius=10,zoom=10)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(mapbox_style=map_style,margin=dict(b=40, t=40, l=20, r=20))
                            return fig
                
                   
                    
           
            hexa_fig = ff.create_hexbin_mapbox(data_frame=data,  lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
            hexa_fig.update_layout(mapbox_style=map_style)
            hexa_fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
            column_names = ['lat','lons','data']
            df = pd.DataFrame(columns = column_names)
            hexa_map_children_list,hexa_map_input_list = [],[]
            hexa_map_children_list.append(dbc.Row(html.H4("Filtration",style={"margin-top":"5%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            for i in columns_name:
                hexa_map_children_list.append(html.Div(children=i, className="menu-title",
                    style={"text-align":"center","color":comb['text_color1'],"margin-top":"5px","padding": "0px 20px",'font-weight': '400'}))
                hexa_map_children_list.append(dcc.Dropdown(
                                id="{}-filter".format(i),
                                options=[
                                    {"label": region, "value": region}
                                    for region in data[i].unique()
                                    # for region in sorted(data[i].unique())
                                ],
                                value=[b for b in data[i].unique()],
                                # value=[b for b in sorted(data[i].unique())],
                                # value="Albany",
                                clearable=False,
                                className="dropdown",
                                style={'background-color':comb['dropdown_color'],'border':'0px'}
                            ),
                    )
                hexa_map_input_list.append(Input("{}-filter".format(i),"value"))
            hexa_map_children_list.append(dbc.Row(html.H4("More Map Options",style={"margin-top":"10%","margin-left":"5%","color":comb['text_color1'],"font-size":"20px",'font-weight': '400'})))
            hexa_map_children_list.append(dbc.Row([dbc.Col(dcc.Link('DensityMap', href='/DensityMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0}),
                    dbc.Col(dcc.Link('ScatterMap', href='/ScatterMap',style={"background-color":comb['botton_on_map_color'],"color": comb['text_color1'],"padding": "14px 20px","text-align": "center","text-decoration": "none","display": "inline"}),width={'size':3.5,'offset':0})],justify="around",style={'margin-top':'5%','margin-bottom':'10%'}))
            hexagon_map_layout = html.Div([dbc.Row([dbc.Col(html.Img(src=logo_image,style={'width':'120px','height':'36px'})),
                dbc.Col(html.H3("Hexagon Map",style={"margin-top":"2%","color":comb['h_color'],"font-size":"40px",'font-family':'TimesNewRoman','font-weight': '700'}))],justify="start"),
                dbc.Row([dbc.Col(children=hexa_map_children_list,width={'size':3,'offset':0.5},style={'background-color':comb['botton_bg_color']}),
                dbc.Col(dcc.Graph(id='hexa-graph',figure=hexa_fig,config={'displayModeBar': False},style={'height':'90vh'}),width={'size':8,'offset':0})],justify="center"),
            ])
            @app.callback(Output("hexa-graph", "figure"),hexa_map_input_list)
            def hexamap_update(*args,**kwargs):
                # 
                if None not in args:
                    if len(args) ==2:
                        if type(args[0])==list and type(args[1])==list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1]))]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==1:
                        if type(args[0])==list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[data[columns_name[0]] == args[0]]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==3:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            # nd = data[((data[columns_name[0]] == args[0])|(data[columns_name[1]] == args[0]) | (data[columns_name[2]] == args[0]))&((data[columns_name[0]] == args[1]) |(data[columns_name[1]] == args[1]) | (data[columns_name[2]] == args[1]))]
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2]))]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==4:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            # nd = data[((data[columns_name[0]] == args[0])|(data[columns_name[1]] == args[0]) | (data[columns_name[3]] == args[0]) | (data[columns_name[3]] == args[0]))&((data[columns_name[0]] == args[1]) |(data[columns_name[1]] == args[1]) | (data[columns_name[2]] == args[1]) | (data[columns_name[3]] == args[1]))]
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3]))]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==5:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4]))]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==6:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5]))]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==7:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6]))]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==8:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7]))]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    elif len(args) ==9:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) ]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
                    
                    elif len(args) ==10:
                        if type(args[0])==list and type(args[1])==list and type(args[2]) == list and type(args[3]) == list and type(args[4]) == list and type(args[5]) == list and type(args[6]) == list and type(args[7]) == list and type(args[8]) == list and type(args[9]) == list:
                            fig=ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                            fig.update_layout(mapbox_style=map_style)
                            fig.update_layout(margin=dict(b=40, t=40, l=40, r=40))
                            # fig = ff.create_hexbin_mapbox(data_frame=data, lat=lcn, lon=longcn,nx_hexagon=30, opacity=0.9,labels={"color": "{}".format(columns_name[1])})
                            return fig
                        else:
                            nd = data[((data[columns_name[0]] == args[0]))&((data[columns_name[1]] == args[1])) & ((data[columns_name[2]] == args[2])) & ((data[columns_name[3]] == args[3])) & ((data[columns_name[4]] == args[4])) & ((data[columns_name[5]] == args[5])) & ((data[columns_name[6]] == args[6])) & ((data[columns_name[7]] == args[7])) & ((data[columns_name[8]] == args[8])) & ((data[columns_name[9]] == args[9])) ]
                            if len(nd) > 0:
                                fig=ff.create_hexbin_mapbox(data_frame=nd, lat=lcn, lon=longcn,nx_hexagon=30, opacity=1,labels={"color":hover_properties},color=hover_properties,zoom=8)
                                return fig
                            else:
                                fig = px.density_mapbox(df, lat='lat', lon='lons', z='data', radius=10,zoom=10)
                                return fig
            
              
            @app.callback(dash.dependencies.Output('page-content', 'children'),[dash.dependencies.Input('url', 'pathname')])
            def display_page(pathname):
                if pathname == '/ScatterMap':
                    return scatter_map_layout
                elif pathname == '/DensityMap':
                    return density_map_layout
                elif pathname == '/HexagonMap':
                    return hexagon_map_layout
                else:
                    return index_page
            app.run_server(debug=False)
        