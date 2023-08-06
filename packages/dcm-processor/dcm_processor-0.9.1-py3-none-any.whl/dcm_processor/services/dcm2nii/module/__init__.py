import os, json
import glob
import pydicom
from .lib import BytesEncoder, remove_strange_tags

DATA = os.getenv("DATA")
dir_path = os.path.dirname(os.path.realpath(__file__))

def load_json(filename):
  data = {}
  with open(filename, 'r') as jsfile:
    data = json.load(jsfile)
  return data

def worker(jobName, headers, params, added_params, **kwargs):
  a_params = added_params.get(jobName)
  
  if (not DATA is None) and (not a_params is None):
    if "conversions" in a_params:
      conversions = a_params.get("conversions", {})
      for k in conversions.keys():
        info = conversions.get(k, {})    
        base = info.get("base")
        filename = info.get("filename")
        ext = info.get("ext", ".nii.gz")
        dcmpath = headers.get("dcmpath")

        if (not base is None) and (not filename is None) and (not dcmpath is None):
          dcm2niix = os.path.join(dir_path, "dcm2niix")
          fullbase = os.path.join(DATA, base)
          tmpfolder = os.path.join(fullbase, filename)
          fulldcmpath = os.path.join(DATA, dcmpath, k)
          command = f"{dcm2niix} -z y -b y -f {filename} -o {tmpfolder} {fulldcmpath}"
          os.system(f"mkdir -p {tmpfolder}")
          os.system(command)
          selected_file = get_max_file(tmpfolder)
          dcm2niix_json_data = {}
          if not selected_file is None:
            fullFilename = f"{filename}{ext}"
            json_filename = str(selected_file).strip().replace(".nii.gz", ".json")
          
            if os.path.isfile(json_filename):
              dcm2niix_json_data = load_json(json_filename)

            os.system(f"mv {selected_file} {os.path.join(fullbase, fullFilename)}")
            os.system(f"rm -rf {tmpfolder}")
          
          searchText = os.path.join(fulldcmpath, "*.dcm")
          filenames = glob.glob(searchText)

          if len(filenames) > 0:
            dcmElem = pydicom.dcmread(filenames[0])
            json_dict = get_dicom_tags(dcmElem)
            json_dict.update(dcm2niix_json_data)
            json_dict = remove_strange_tags(json_dict)
            with open(os.path.join(fullbase, f"{filename}.json"), "w") as outfile:
              json.dump(json_dict, outfile, cls=BytesEncoder, indent=4, sort_keys=True)

def get_dicom_tags(dcmElem: pydicom.Dataset, excTags=None):
  baseTypes = [bytes, float, int, list, str]
  convertTypes = {
    pydicom.uid.UID: str,
    pydicom.valuerep.DSfloat: float,
    pydicom.valuerep.IS: int,
    pydicom.valuerep.PersonName: str,
    pydicom.multival.MultiValue : list,
    pydicom.sequence.Sequence: list
  }

  data = {}
  exc = [] if excTags is None else excTags
  for elem in dcmElem:
    name = "".join(str(elem.name).split(" "))
    if (elem.name in exc) or (name in exc):
      continue

    if elem.VR == 'OW':
      data[name] = None
      continue

    if elem.VR == 'SQ':
      items = []
      for el in elem.value:
        value = get_dicom_tags(el, excTags)
        items.append(value)
      data[name] = items
    else:
      elemType = type(elem.value)
      if elemType in baseTypes:
        data[name] = elem.value
      elif elemType in convertTypes:
        data[name] = convertTypes[elemType](elem.value)
      else:
        data[name] = str(elem.value)

  return data

def get_max_file(searchpath):
  searchText = os.path.join(searchpath, "*.nii.gz")
  filenames = glob.glob(searchText)
  if len(filenames) == 1:
    return filenames[0]
  elif len(filenames) > 1:
    ind = 0
    m_size = os.path.getsize(filenames[0])
    for i in range(1, len(filenames)):
      c_size = os.path.getsize(filenames[i])
      if c_size > m_size:
        ind = i
        m_size = c_size
    return filenames[ind]
  else:
    return None