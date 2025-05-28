import arcpy
import pyodbc
'''This python code loops over feature classes in a geodatabase'''

mdb_path = r"C:\Users\rig1\Downloads\SouthernLots.mdb"
output_gdb = r"C:\Users\rig1\temp20250528.gdb"  # Existing FGDB

# Connect and get tables from MDB
conn_str = (
    r'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};'
    r'DBQ={};'.format(mdb_path)
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
tables = [row.table_name for row in cursor.tables(tableType='TABLE')]
cursor.close()
conn.close()

print("Tables / Feature classes in MDB:")
for table in tables:
    print(table)

# Loop through tables and quick import each one separately using arcpy.interop.QuickImport
for fc in tables:
    try:
        print(f"Importing {fc} ...")
        #arcpy.interop.QuickImport(
         #   Input=mdb_path,
         #   Output=output_gdb,
         #   IDList=[fc]  # Just import this single feature class
        #)
        arcpy.interop.QuickImport(
            Input=r'PERSONAL_GEODATABASE,"C:\Users\rig1\Downloads\Southern Lots Geo.mdb","RUNTIME_MACROS,""TABLELIST,points,WHERE_CLAUSE,,EXPOSE_ATTRS_GROUP,,PERSONAL_GEODATABASE_EXPOSE_FORMAT_ATTRS,,USE_SEARCH_ENVELOPE,NO,SEARCH_ENVELOPE_MINX,0,SEARCH_ENVELOPE_MINY,0,SEARCH_ENVELOPE_MAXX,0,SEARCH_ENVELOPE_MAXY,0,SEARCH_ENVELOPE_COORDINATE_SYSTEM,,CLIP_TO_ENVELOPE,NO,READ_BOOLEANS_AS_YES_NO,YES,READ_NULLS,YES,EXPOSE_PRIMARY_KEY_ATTRIBUTE,NO,QUERY_FEATURE_TYPES_FOR_MERGE_FILTERS,Yes,ADVANCED,,DONUT_DETECTION,ORIENTATION,_MERGE_SCHEMAS,YES"",META_MACROS,""SourceWHERE_CLAUSE,,SourceEXPOSE_ATTRS_GROUP,,SourcePERSONAL_GEODATABASE_EXPOSE_FORMAT_ATTRS,,SourceUSE_SEARCH_ENVELOPE,NO,SourceSEARCH_ENVELOPE_MINX,0,SourceSEARCH_ENVELOPE_MINY,0,SourceSEARCH_ENVELOPE_MAXX,0,SourceSEARCH_ENVELOPE_MAXY,0,SourceSEARCH_ENVELOPE_COORDINATE_SYSTEM,,SourceCLIP_TO_ENVELOPE,NO,SourceREAD_BOOLEANS_AS_YES_NO,YES,SourceREAD_NULLS,YES,SourceEXPOSE_PRIMARY_KEY_ATTRIBUTE,NO,SourceQUERY_FEATURE_TYPES_FOR_MERGE_FILTERS,Yes,SourceADVANCED,,SourceDONUT_DETECTION,ORIENTATION"",METAFILE,PERSONAL_GEODATABASE,COORDSYS,,IDLIST,points,__FME_DATASET_IS_SOURCE__,true"',
            Output=r"C:\Users\rig1\Downloads\southern_lots_geo_second_college_grant2.gdb"
        )
        arcpy.interop.QuickImport(
            Input=(
                f'PERSONAL_GEODATABASE,"{mdb_path}","RUNTIME_MACROS,""TABLELIST,{fc},WHERE_CLAUSE,,EXPOSE_ATTRS_GROUP,,'
                f'PERSONAL_GEODATABASE_EXPOSE_FORMAT_ATTRS,,USE_SEARCH_ENVELOPE,NO,SEARCH_ENVELOPE_MINX,0,SEARCH_ENVELOPE_MINY,0,'
                f'SEARCH_ENVELOPE_MAXX,0,SEARCH_ENVELOPE_MAXY,0,SEARCH_ENVELOPE_COORDINATE_SYSTEM,,CLIP_TO_ENVELOPE,NO,'
                f'READ_BOOLEANS_AS_YES_NO,YES,READ_NULLS,YES,EXPOSE_PRIMARY_KEY_ATTRIBUTE,NO,QUERY_FEATURE_TYPES_FOR_MERGE_FILTERS,Yes,'
                f'ADVANCED,,DONUT_DETECTION,ORIENTATION,_MERGE_SCHEMAS,YES"",META_MACROS,""SourceWHERE_CLAUSE,,SourceEXPOSE_ATTRS_GROUP,,'
                f'SourcePERSONAL_GEODATABASE_EXPOSE_FORMAT_ATTRS,,SourceUSE_SEARCH_ENVELOPE,NO,SourceSEARCH_ENVELOPE_MINX,0,'
                f'SourceSEARCH_ENVELOPE_MINY,0,SourceSEARCH_ENVELOPE_MAXX,0,SourceSEARCH_ENVELOPE_MAXY,0,SourceSEARCH_ENVELOPE_COORDINATE_SYSTEM,,'
                f'SourceCLIP_TO_ENVELOPE,NO,SourceREAD_BOOLEANS_AS_YES_NO,YES,SourceREAD_NULLS,YES,SourceEXPOSE_PRIMARY_KEY_ATTRIBUTE,NO,'
                f'SourceQUERY_FEATURE_TYPES_FOR_MERGE_FILTERS,Yes,SourceADVANCED,,SourceDONUT_DETECTION,ORIENTATION"",'
                f'METAFILE,PERSONAL_GEODATABASE,COORDSYS,,IDLIST,{fc},__FME_DATASET_IS_SOURCE__,true"'
                ),
            Output=output_gdb
        )
        print(f"Successfully imported {fc}")
    except Exception as e:
        print(f"fc failed, fc name is {fc}")
        print("Error:", e)
        continue
