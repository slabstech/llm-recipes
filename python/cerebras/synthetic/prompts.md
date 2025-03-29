
t-50 tank in a camouflage forest environment avoiding detection

curl -X 'GET' \
  'https://slabstech-image-gen.hf.space/generate?prompt=t-50%20tank%20in%20a%20camouflage%20forest%20environment%20avoiding%20detection' \
  -H 'accept: application/json'


quadcopters surrounding soldiers

  curl -X 'GET' \
  'https://slabstech-image-gen.hf.space/generate?prompt=quadcopters%20surrounding%20soldiers' \
  -H 'accept: application/json'


  -

  Tank Grey

curl -X 'POST' \
  'https://slabstech-image-gen-edit.hf.space/edit-image/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@1200px-T-55_4.jpg;type=image/jpeg' \
  -F 'instruction=make it grey' \
  -F 'steps=5' \
  -F 'text_cfg_scale=7.5' \
  -F 'image_cfg_scale=1.5' \
  -F 'seed=1371' -o tank_grey.jpg


Tank White



- Snow weather

curl -X 'POST' \
  'https://slabstech-image-gen-edit.hf.space/edit-image/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@1200px-T-55_4.jpg;type=image/jpeg' \
  -F 'instruction=make it camoflage in snow weather' \
  -F 'steps=5' \
  -F 'text_cfg_scale=7.5' \
  -F 'image_cfg_scale=1.5' \
  -F 'seed=1371' -o snow_weater.jpg




--

curl -X POST "https://slabstech-image-gen-edit.hf.space/inpaint/" \
  -F "file=@1200px-T-55_4.jpg;type=image/jpeg" \
  -F "prompt=a lush green forest" \
  -F "mask_coordinates=100,100,300,300" \
  -o inpainted_image.png

