# database utilities 
# log in to Dartmouth RDS or open ArcGIS Pro 
# 
import arcpy
arcpy.interop.QuickImport()
# parameters: 

##############
arcpy.interop.QuickImport(
    Input=r'PERSONAL_GEODATABASE,"C:\Users\rig1\Downloads\Grant Infrastructure.mdb","RUNTIME_MACROS,""TABLELIST,Above_2500_in_Natural_Areas,WHERE_CLAUSE,,EXPOSE_ATTRS_GROUP,,PERSONAL_GEODATABASE_EXPOSE_FORMAT_ATTRS,,USE_SEARCH_ENVELOPE,NO,SEARCH_ENVELOPE_MINX,0,SEARCH_ENVELOPE_MINY,0,SEARCH_ENVELOPE_MAXX,0,SEARCH_ENVELOPE_MAXY,0,SEARCH_ENVELOPE_COORDINATE_SYSTEM,,CLIP_TO_ENVELOPE,NO,READ_BOOLEANS_AS_YES_NO,YES,READ_NULLS,YES,EXPOSE_PRIMARY_KEY_ATTRIBUTE,NO,QUERY_FEATURE_TYPES_FOR_MERGE_FILTERS,Yes,ADVANCED,,DONUT_DETECTION,ORIENTATION,_MERGE_SCHEMAS,YES"",META_MACROS,""SourceWHERE_CLAUSE,,SourceEXPOSE_ATTRS_GROUP,,SourcePERSONAL_GEODATABASE_EXPOSE_FORMAT_ATTRS,,SourceUSE_SEARCH_ENVELOPE,NO,SourceSEARCH_ENVELOPE_MINX,0,SourceSEARCH_ENVELOPE_MINY,0,SourceSEARCH_ENVELOPE_MAXX,0,SourceSEARCH_ENVELOPE_MAXY,0,SourceSEARCH_ENVELOPE_COORDINATE_SYSTEM,,SourceCLIP_TO_ENVELOPE,NO,SourceREAD_BOOLEANS_AS_YES_NO,YES,SourceREAD_NULLS,YES,SourceEXPOSE_PRIMARY_KEY_ATTRIBUTE,NO,SourceQUERY_FEATURE_TYPES_FOR_MERGE_FILTERS,Yes,SourceADVANCED,,SourceDONUT_DETECTION,ORIENTATION"",METAFILE,PERSONAL_GEODATABASE,COORDSYS,,IDLIST,Above_2500_in_Natural_Areas,__FME_DATASET_IS_SOURCE__,true"',
    Output=r"V:\home\9\f002d69\projects\patry\results\grant_infrastructure_results_etl20250527.gdb"
)

#############

arcpy.management.Copy(
    in_data=r"C:\Users\rig1\Documents\temp_grants.gdb",
    out_data=r"C:\Users\rig1\Documents\temp_grants_combined.gdb",
    data_type="Workspace",
    associated_data=None
)

##############
import arcpy

gdb_path = r"C:\path\to\your.gdb"
gdb_path = r"C:\Users\rig1\Documents\temp\temp_grants.gdb"

arcpy.env.workspace = gdb_path

all_layers = []

# Feature classes in the root of the geodatabase
feature_classes = arcpy.ListFeatureClasses()
if feature_classes:
    all_layers.extend(feature_classes)

# Feature classes inside feature datasets
feature_datasets = arcpy.ListDatasets(feature_type='feature')
if feature_datasets:
    for fds in feature_datasets:
        arcpy.env.workspace = f"{gdb_path}\\{fds}"
        fcs_in_fds = arcpy.ListFeatureClasses()
        if fcs_in_fds:
            all_layers.extend([f"{fds}\\{fc}" for fc in fcs_in_fds])

# Reset workspace
arcpy.env.workspace = gdb_path

# Sort all layers alphabetically
all_layers_sorted = sorted(all_layers)

# Print sorted list
for layer in all_layers_sorted:
    print(layer)
