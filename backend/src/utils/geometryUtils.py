from shapely.geometry import Polygon, MultiPolygon




def ajusta_lado_x(geom, left_expand=0.0, right_shrink=0.0):
    
    
    def ajusta_pol(pol):
        coords_novas = []
        minx, _, maxx, _ = pol.bounds
        
        
        for x, y in pol.exterior.coords:            
            if abs(x - minx) < 1e-8:
                x -= left_expand
           
            elif abs(x - maxx) < 1e-8:
                x -= right_shrink
            
            coords_novas.append((x, y))
        
        return Polygon(coords_novas)

    
    if geom.geom_type == 'Polygon':
        return ajusta_pol(geom)
   
    elif geom.geom_type == 'MultiPolygon':
        return MultiPolygon([ajusta_pol(p) for p in geom.geoms])
   
    else:
        raise ValueError("Geom deve ser Polygon ou MultiPolygon")





def ajusta_lado_y(geom, bottom_expand=0.0, top_shrink=0.0):
    
    
    def ajusta_pol(pol):
        coords_novas = []
        _, miny, _, maxy = pol.bounds
        
        for x, y in pol.exterior.coords:            
            if abs(y - miny) < 1e-8:
                y -= bottom_expand
            
            elif abs(y - maxy) < 1e-8:
                y -= top_shrink
            coords_novas.append((x, y))
        
        return Polygon(coords_novas)

    
    if geom.geom_type == 'Polygon':
        return ajusta_pol(geom)
    
    elif geom.geom_type == 'MultiPolygon':
        return MultiPolygon([ajusta_pol(p) for p in geom.geoms])
    
    else:
        raise ValueError("Geom deve ser Polygon ou MultiPolygon")



def aplica_buffer(geom, buffer_metros=30.0):

    return geom.buffer(buffer_metros)
