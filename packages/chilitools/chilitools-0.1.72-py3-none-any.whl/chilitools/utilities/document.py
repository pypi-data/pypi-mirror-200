from lxml import etree

class ChiliDocument:
  def __init__(self, doc_xml: str):
    try:
      self.doc: etree._Element = etree.fromstring(doc_xml)
      self.name = self._extract_name()
      self.id = self._extract_id()
    except Exception as e:
      print(f"There was an error creating a Document from the XML\n {e}")

  def _extract_name(self):
    if self.doc is None: return
    return self.doc.attrib.get('name')

  def _extract_id(self):
    if self.doc is None: return
    return self.doc.attrib.get('id')

  def __str__(self) -> str:
    return self.to_xml()

  def to_xml(self) -> str:
    return etree.tostring(self.doc, method="xml", encoding="unicode")

  def get_datasource(self):
    return self.doc.find("dataSource")

  def get_datasource_string(self) -> str:
    return etree.tostring(self.get_datasource(), encoding="unicode")

  def set_datasource(self, new_datasource):
    self.doc.replace(self.doc.find("dataSource"), new_datasource)

  def get_fonts(self):
    if self.doc is None: return
    fonts = []

    for font in self.doc.findall("fonts//"):
      fonts.append({
        "resource_type": "Fonts",
        "id": font.get("id"),
        "name": font.get("name"),
        "family": font.get("family"),
        "style": font.get("style")
      })

    return fonts

  def get_images(self):
    if self.doc is None: return
    images = []

    for image_frame in self.doc.findall("pages//item[@type='image']"):
      if image_frame.get("hasContent", "false") == "true":
        if len(image_frame.get("dynamicAssetProviderID", "")) > 1:
          images.append({
            "resource_type": "DynamicAssetProviders",
            "id": image_frame.get("dynamicAssetProviderID")
          })
        else:
          images.append({
            "resource_type": "Assets",
            "id": image_frame.get("externalID"),
            "name": image_frame.get("externalName", ""),
            "path": image_frame.get("path", "")
          })

    return images
