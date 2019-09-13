from openpyxl import load_workbook
from openpyxl.comments import Comment
import time

# Allegro dataview
from allegroai import Task, DataView, DataPipe, IterationOrder
import json
import video_iter

# Parameters
datasetname = 'guardian'
versionname = 'import-218dabef-8ceb-4de9-a3ee-c9fd7e24a8b7_with_annotations'

file = r"G:\My Drive\Guardian Common repository\R&D\QA\Algorithm test results\OccupancyDetection\OD TER.xlsx"
wb = load_workbook(file)

def q_get_clips_from_allegro(tag_value):
    
    dataview = DataView(iteration_order=IterationOrder.sequential, iteration_infinite=False)
    dataview.add_query(
        dataset_name=datasetname,
        version_name=versionname,
        frame_query="meta.csv_data." + tag_value
    )

    print("Inside Allegro... tag_value=", tag_value, " >>> ", "meta.csv_data." + tag_value)
    value_start = tag_value.find("\"")
    tag = tag_value[0:value_start-1]
    value = tag_value[value_start+1:len(tag_value)-1]
    print("tag=",tag," value=",value)
    
    videos = list(video_iter.get_videos(dataview=dataview))
    print ("# of videos=",len(videos))
    
    x = "meta_frame[\"csv_data\"]" + "[\"" + tag.replace(".","\"][\"") + "\"]"
    print("x=",x)
        
    for imageframe in videos:
        meta_frame = imageframe.meta
        
        try:
            eval_x = eval(x)
        except KeyError:
            print("ERROR ")
            return None
            
        if(eval_x == value):
            print("OK ",end = '')
        else:
            print("NOK ",end = '')
        
        print("[", meta_frame["csv_data"]["seq_id"],"]",end = '')
        # print(" ROI=",imageframe.rois)
        try:
            print("  D=",meta_frame["csv_data"]["Driver_person"]["id"],end = '')
        except KeyError:
            print ("  D=?",end = '')
        try:
            print(" FR=",meta_frame["csv_data"]["FR_person"]["id"],end = '')
        except KeyError:
            print (" FR=?",end = '')
        try:
            print(" RL=",meta_frame["csv_data"]["RL_person"]["id"],end = '')
        except KeyError:
            print (" RL=?",end = '')
        try:
            print(" MS=",meta_frame["csv_data"]["MS_person"]["id"],end = '')
        except KeyError:
            print (" MS=?",end = '')
        try:
            print(" RR=",meta_frame["csv_data"]["RR_person"]["id"])
        except KeyError:
            print (" RR=?")

changes = False
for sheet in wb.worksheets:
    if (sheet.title.startswith("TC - ")):
        print("Found {0} analyzing cells...".format(sheet.title))
		
        for r in sheet.rows:
            for c in r:
                if (type(c.value) == str and c.value.startswith("%")):
                    print(c.value)
                    print(c.value[1:])
                    q_get_clips_from_allegro(c.value[1:])
                    c.comment = Comment("executed on [{0}]".format(time.time()), 'Zvika Melamed')
                    changes = True

if (changes):
	wb.save(file)
