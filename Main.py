from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest, SHConfig
from PIL import Image

config = SHConfig()
config.sh_client_id = '578f0dfe-c2cb-4811-9d74-42cc91f4f226'
config.sh_client_secret = 'ZKzp+hD+|JPUPjJgH]n<:t3EUiC?}QCC/ULNrD.~'

coords_wgs84 = [23.439760, 41.901768, 23.550828, 41.851160]
resolution = 10
bbox = BBox(bbox=coords_wgs84, crs=CRS.WGS84)
size = bbox_to_dimensions(bbox, resolution=resolution)

print(f'Image shape at {resolution} m resolution: {size} pixels')

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B08", "B04", "B03"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B08, sample.B04, sample.B03];
    }
"""

request_true_color = SentinelHubRequest(
    evalscript = evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=('2021-08-05', '2021-08-06'),
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=bbox,
    size=size,
    config=config
)

true_color_imgs = request_true_color.get_data()

image = true_color_imgs[0]
print(type(image))
img = Image.fromarray(image, "RGB")
img.save('img1.png')
img.show()
# plt.imshow(image,interpolation="nearest")
# plt.show()
# print()
