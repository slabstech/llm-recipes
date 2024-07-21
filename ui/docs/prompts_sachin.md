Prompt 1

https://www.alamy.com/fruit-stall-cochin-kerala-india-image235118669.html?imageid=0EBBBAFA-DD25-4FF9-B566-9F6854BA424F

- Reference - Multi shot prompt

- https://huggingface.co/spaces/MrOvkill/moondream-2-multi-interrogation/blob/main/app.py
- https://github.com/zhongpei/Comfyui_image2prompt



"Generate a JSON object that contains details about three different fruits, including their names, colors, and tastes."

- Response

Image processing result: 
 [{"fruit": "banana", "color": "yellow", "taste": "sweet", "type": "fruit"}, 
  {"fruit": "orange", "color": "orange", "taste": "sweet", "type": "fruit"}, 
  {"fruit": "apple", "color": "red", "taste": "sweet", "type": "fruit"}] 


Prompt 2

Please analyze the image and return the results in valid JSON format. Include the following information:
{
  "objects": [list of main objects detected],
  "colors": [list of dominant colors],
  "scene_type": [indoor/outdoor],
  "description": [brief description of the image content],
  "emotions": [any emotions conveyed, if applicable]
}

- Response
Image processing result: 
 [{"type": "fruit", "color": [0.42, 0.3, 0.56, 0.43]}, {"type": "fruit", "color": [0.52, 0.31, 0.61, 0.41]}, ... , {"type": "fruit", "color": [0.68, 0.4, 0.76, 0.48]}}]

Prompt 3

"Generate a JSON object similar to {'name': 'Alice', 'age': 30} but for a different person."


Prompt 4

"Create a JSON object that represents a shopping cart. It should contain an array of items, and each item should be an object with properties for itemName, quantity, and price."

- Respone

 [
  { "itemName": "Bananas", "quantity": 2, "price": 0.25 },
  { "itemName": "Oranges", "quantity": 1, "price": 0.35 },
  ... (additional items) ...
 ]

Prompt 5

"Generate a JSON object for a movie, where the title is a string, the release year is a number, and the genres are an array of strings."


Prompt 6 -  Do not use this, crashes moondream

"List the names of three fruits."
"For each fruit, provide its color and taste."
"Now create a JSON object that includes the fruits’ names, colors, and tastes."

Prompt 7

"Generate a JSON object for a book that includes an array of authors. The array must contain at least two authors."




 Prompt 8

 "Analyse the image and Generate a JSON object that contains details about all the different fruits, including their names, colors, and tastes."