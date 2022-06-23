import json

OG_SIZE = [0,0]
NEW_SIZE =  [1200, 2400]
with open('instances_default_copy.json', 'r+') as file:
    data = json.load(file)
    for annotation in data['annotations']:
        image_id = annotation['image_id']
        assert data['images'][image_id-1]['id']==image_id
        OG_SIZE[0] = data['images'][image_id-1]["width"]
        OG_SIZE[1] = data['images'][image_id-1]["height"]

    
        if OG_SIZE[1]/OG_SIZE[0] > NEW_SIZE[1]/NEW_SIZE[0]: #x_padding
            ratio = NEW_SIZE[1]/OG_SIZE[1]
            #\/\/--------------------segmentation-----------------\/\/#
            segmentation = annotation['segmentation'][0]
            for x in range(4):
                segmentation[2*x] = round(segmentation[2*x]*ratio + (NEW_SIZE[0] - OG_SIZE[0]*ratio)/2, 1)
            for y in range(4):
                segmentation[2*y+1] = round(segmentation[2*y+1]*ratio, 1)
            #\/\/----------------------area-----------------------\/\/#
            annotation['area'] = round(annotation['area']*ratio*ratio, 1)
            #\/\/-----------------bounding box--------------------\/\/#
            for i in range(0,3,2): #i=0,2
                annotation['bbox'][i] = round(annotation['bbox'][i]*ratio + (NEW_SIZE[0] - OG_SIZE[0]*ratio)/2, 1)
            for j in range(1,4,2): #j=1,3
                annotation['bbox'][j] = round(annotation['bbox'][j]*ratio, 1)
        
        elif OG_SIZE[1]/OG_SIZE[0] < NEW_SIZE[1]/NEW_SIZE[0]: #y_padding
            ratio = NEW_SIZE[0]/OG_SIZE[0]
            #\/\/--------------------segmentation-----------------\/\/#
            segmentation = annotation['segmentation'][0]
            for x in range(4):
                segmentation[2*x] = round(segmentation[2*x]*ratio, 1)
            for y in range(4):
                segmentation[2*y+1] = round(segmentation[2*y+1]*ratio + (NEW_SIZE[1] - OG_SIZE[1]*ratio)/2, 1)
            #\/\/----------------------area-----------------------\/\/#
            annotation['area'] = round(annotation['area']*ratio*ratio, 1)
            #\/\/-----------------bounding box--------------------\/\/#
            for i in range(0,3,2): #i=0,2
                annotation['bbox'][i] = round(annotation['bbox'][i]*ratio, 1)
            for j in range(1,4,2): #j=1,3
                annotation['bbox'][j] = round(annotation['bbox'][j]*ratio + (NEW_SIZE[1] - OG_SIZE[1]*ratio)/2, 1)

        # for x in range(4):
        #     segmentation[2*x] = segmentation[2*x]/OG_SIZE[0]*NEW_SIZE[0]
        # for y in range(4):
        #     segmentation[2*y+1] = segmentation[2*y+1]/OG_SIZE[1]*NEW_SIZE[1]

    file.seek(0)
    json.dump(data, file)
    file.truncate()