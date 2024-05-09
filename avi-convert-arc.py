import arcpy
import subprocess
import os

def convert_avi_to_mp4(vlc_path, input_file, output_file):
    command = [vlc_path, input_file, '--sout', f'#transcode{{vcodec=h264,vb=800,acodec=mp4a,ab=128,channels=2,samplerate=44100}}:std{{access=file,mux=mp4,dst={output_file}}}']
    subprocess.run(command)

def convert_blobs_in_table(gdb_path, table_name, blob_field, att_field, vlc_path):
    # Set workspace
    arcpy.env.workspace = gdb_path

    # List all rows in the table
    with arcpy.da.UpdateCursor(table_name, [blob_field, att_field]) as cursor:
        for row in cursor:
            blob_data = row[0]
            if blob_data is not None:
                # Write the blob data to a temporary .avi file
                input_file = row[1]
                with open(input_file, 'wb') as file:
                    file.write(blob_data.tobytes())

                # Convert the .avi file to .mp4
                output_file = row[1].replace('.avi', '.mp4')
                convert_avi_to_mp4(vlc_path, input_file, output_file)

                # Update the ATT_NAME and DATA fields
                with open(output_file, 'rb') as file:
                    row[2] = file.read()

                # Update the row
                cursor.updateRow(row)

                # Delete the temporary .avi file
                os.remove(input_file)

def get_tables_with_blobs(gdb_path):
    # Set workspace
    arcpy.env.workspace = gdb_path

    # Get all tables
    tables = arcpy.ListTables()

    # Filter tables that have a blob field
    tables_with_blobs = []
    for table in tables:
        fields = arcpy.ListFields(table)
        for field in fields:
            if field.type == 'Blob':
                tables_with_blobs.append(table)
                break

    return tables_with_blobs

# Usage example
gdb_path = 'C:/path/to/your.gdb'
vlc_path = 'C:/Program Files/VideoLAN/VLC/vlc.exe'
tables_with_blobs = get_tables_with_blobs(gdb_path)
for table in tables_with_blobs:
    # get blob field name and attachment field name
    fields = arcpy.ListFields(table)
    for field in fields:
        if field.type == 'Blob':
            blob_field = field.name
        if field.type == 'String' and (field.name.endswith('.avi') or field.name.endswith('.mp4')):
            att_field = field.name
        if att_field is not None and blob_field is not None:
            convert_blobs_in_table(gdb_path, table, blob_field, att_field, vlc_path)
            break