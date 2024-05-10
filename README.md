# AVI to MP4 Converter for ArcGIS

This Python script provides functionality to convert .avi video files stored as blob data in an ArcGIS geodatabase to .mp4 format using VLC.

## 🚀 Features

- Converts .avi files to .mp4 using VLC.
- Updates the geodatabase table with the new .mp4 file data.
- Works with any geodatabase table that contains blob data.

## 📋 Requirements

- ArcGIS Pro with ArcPy
- VLC Media Player
- Python 3

## 📖 Usage

1. **Import the necessary modules:**

```python
import arcpy
import subprocess
import os
```

2. **Define the conversion function:**
```def convert_avi_to_mp4(vlc_path, input_file, output_file):
    command = [vlc_path, input_file, '--sout', f'#transcode{{vcodec=h264,vb=800,acodec=mp4a,ab=128,channels=2,samplerate=44100}}:std{{access=file,mux=mp4,dst={output_file}}}']
    subprocess.run(command)
    ```
3. **Define the function to convert blobs in a table:**

```def convert_blobs_in_table(gdb_path, table_name, blob_field, att_field, vlc_path):
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
                ```

4. **Execute the `convert_blobs_in_table` function:**

    Replace the placeholders with your actual values:

    - `gdb_path`: Path to your geodatabase (e.g., `'C:/path/to/your.gdb'`)
    - `table_name`: Name of your table (e.g., `'your_table'`)
    - `blob_field`: Name of your blob field (e.g., `'your_blob_field'`)
    - `att_field`: Name of your attachment field (e.g., `'your_attachment_field'`)
    - `vlc_path`: Path to VLC (e.g., `'C:/Program Files/VideoLAN/VLC/vlc.exe'`)

    ```python
    gdb_path = 'C:/path/to/your.gdb'
    table_name = 'your_table'
    blob_field = 'your_blob_field'
    att_field = 'your_attachment_field'
    vlc_path = 'C:/Program Files/VideoLAN/VLC/vlc.exe'

    convert_blobs_in_table(gdb_path, table_name, blob_field, att_field, vlc_path)
    ```

## 📜 License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for more details.