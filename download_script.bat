#########################################################
##
## Pipeline to download CTs, CXRs from PACS using dcm4che
##
#########################################################


## Reference websites:
## https://support.dcmtk.org/docs/getscu.html
## https://pydicom.github.io/pynetdicom/dev/apps/getscu.html

## getscu reference command:
# getscu -c DICOM_QR_SCP@161.62.16.7:104 -m StudyInstanceUID=1.2.826.0.1.3680043.11.105


#########################################################
## dcm4che directory:
# C:\Users\i0312119\Downloads\dcm4che-5.27.0-bin\dcm4che-5.27.0\bin

## First command
getscu -c DICOM_QR_SCP@161.62.16.7:7840 -m StudyInstanceUID=6028057

## Output with the First command
# RoleSelection[
#    sopClass: 1.2.840.10008.5.1.4.1.1.2 - CT Image Storage
#    scu: false
#    scp: true
#  ]
#  RoleSelection[
#    sopClass: 1.2.840.10008.5.1.4.1.1.1 - Computed Radiography Image Storage
#    scu: false
#    scp: true
#  ]


#########################################################
## Other alternatives
# movescu -c DICOM_QR_SCP@161.62.16.7:7840 -m StudyInstanceUID=6028057  --output-directory "\\filer300\users3005\i0312119\Documents\dicom-query-files"
# movescu -c DICOM_QR_SCP@161.62.16.7:7840 -m StudyInstanceUID=6028057 --dest \\filer300\users3005\i0312119\Documents\dicom-query-files
# getscu -c DICOM_QR_SCP@161.62.16.7:7840 -k (0008,0052)=10130705 peer port dcmfile-in "\\filer300\users3005\i0312119\Documents\dicom-query-files"
