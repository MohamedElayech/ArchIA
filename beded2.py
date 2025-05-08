import zlib
import base64
import urllib.parse


def drawio_to_url(output_file):
  # Load your .drawio file (which is XML inside)
  with open(output_file, "r", encoding="utf-8") as file:
      xml_content = file.read()

  # Compress using raw DEFLATE (no zlib headers/footers)
  compressor = zlib.compressobj(wbits=-15)
  compressed_data = compressor.compress(xml_content.encode('utf-8')) + compressor.flush()

  # Base64 encode the compressed data
  b64_encoded_data = base64.b64encode(compressed_data).decode('utf-8')

  # URL-encode the base64 data
  url_encoded_data = urllib.parse.quote(b64_encoded_data, safe='')

  # Create the final iframe-compatible src URL
  iframe_src = f"https://viewer.diagrams.net/?lightbox=1&edit=_blank&layers=1&nav=1#R{url_encoded_data}"
  drawio_link = f"https://app.diagrams.net/?lightbox=1&edit=_blank&layers=1&nav=1#R{url_encoded_data}"
  return drawio_link
  # print(drawio_link)
  # # Generate the HTML
  # html_output = f"""
  # <!DOCTYPE html>
  # <html>
  #   <head>
  #     <title>Embedded Draw.io</title>
  #   </head>
  #   <body>
  #     <!-- draw.io diagram -->
  #     <iframe
  #       frameborder="0"
  #       style="width: 100%; height: 100vh"
  #       src="{iframe_src}"
  #     ></iframe>
  #   </body>
  # </html>
  # """

  # # Write the output HTML file
  # with open("diagram_embed_inshallah.html", "w", encoding="utf-8") as file:
  #     file.write(html_output)

  # print(" Done! 'diagram_embed.html' created.")
