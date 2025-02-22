openapi: 3.0.0
info:
  title: Zomato API
  description: "This is a Zomato RESTful API. It gives you the freshest and most exhaustive\
    \ restaurant content to power your applications with. It covers 1.5 million restaurants\
    \ across 10,000 cities globally.This RESTful API searches for restaurants by name,\
    \ cuisine, or location, a detailed information including ratings, location and\
    \ cuisine. You can get free and instant access to restaurant information by requesting\
    \ the [`access-key`](https://developers.zomato.com/api).\n\n# Concepts\n\nThe\
    \ Zomato Web-API utilizes standard HTTP communication and uses REST concepts.\
    \ Requests and responses contain JSON in the HTTP body. The character encoding\
    \ is always UTF8. Ensure that your client is capable of handling SSL/TLS HTTP\
    \ requests.\n\n**API-Key**\n\nAn API-Key is a long-lasting secret that represents\
    \ a unique id. An authorized user can generate a key in Zomato-API for his usage.\
    \ The user should place this secret in your application settings. Important: Keep\
    \ this API-Key secret! The application then uses this api-key in each request\
    \ that is made with our api.\n\n**Example HTTP Header**\n\n    Authorization:\
    \ Bearer <API-Key or Access Token>\n    Accept: application/json\n# HTTP Request\
    \ examples\nRequests that don’t have side-effects (and do not change anything)\
    \ utilize\nthe `GET` method.\n\n**Read example**\n\n    GET /api/v2.1/categories\n\
    \    Host: developers.zomato.com\n    Authorization: Bearer 5ffb698e3d9a8ea8d51fb8847c216058\n\
    \    Accept: application/json\n# HTTP Response body\n\nEvery HTTP response is\
    \ wrapped by a response body. You should evaluate the success value to check if\
    \ the operation was successful. If there was a failure an error object will be\
    \ returned. \n\nFor successful operations we will return the data for read operations.\
    \ For read operations a corresponding object will be returned if the data is a\
    \ array of multiple items.\n\nExample HTTP Response with single expected result\
    \ or single affected entity\n\n    HTTP/2 200 OK\n    Content-Type: application/json\n\
    \n    {\n        \"success\": true,\n        \"data\": {\n            \"id\":\
    \ 1234,\n             ...\n        }\n    }\n  \n # Error handling\n\n\nEnsure\
    \ to evalute the http status code and react on them accordingly. See table below.\
    \ If there is an error code that is not 200, there might not be a response body.\n\
    \nHowever if there is a response body `success` should be `false` and we return\
    \ a error with additional information what went wrong. \n"
  termsOfService: https://www.zomato.com/api_policy
  contact:
    email: vivekraj3200@gmail.com
  license:
    name: Apache 2.0
    url: http://www.apache.org/licenses/LICENSE-2.0.html
  version: 1.0.0-oas3
externalDocs:
  description: Find out more about Swagger
  url: http://swagger.io
servers:
- url: https://developers.zomato.com/api/v2.1
- url: http://developers.zomato.com/api/v2.1
paths:
  /categories:
    get:
      tags:
      - Categories
      summary: Get list of Categories
      operationId: getlist
      parameters:
      - name: user-key
        in: header
        description: Get a list of categories. List of all restaurants categorized
          under a particular restaurant type can be obtained using /Search API with
          Category ID as inputs.
        required: true
        style: simple
        explode: false
        schema:
          type: string
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Categories'
            application/xml:
              schema:
                $ref: '#/components/schemas/Categories'
        "403":
          description: Invalid Key.
  /cities:
    get:
      tags:
      - Cities
      summary: Find the Zomato ID and other details for a city.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: q
        in: query
        description: query by city name
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: lat
        in: query
        description: latitude
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: lon
        in: query
        description: longitude
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: city_ids
        in: query
        description: comma separated city_id values
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: count
        in: query
        description: number of max results to display
        required: false
        style: form
        explode: true
        schema:
          type: integer
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Cities'
            application/xml:
              schema:
                $ref: '#/components/schemas/Cities'
        "403":
          description: Invalid Key.
  /collections:
    get:
      tags:
      - Collections
      summary: Returns Zomato Restaurant Collections in a City.
      description: List of all restaurants listed in any particular Zomato Collection
        can be obtained using the '/search' API with Collection ID and Zomato City
        ID as the input.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: lat
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: lon
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: city_id
        in: query
        description: id of the city for which collections are needed
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: count
        in: query
        description: number of max results to display
        required: false
        style: form
        explode: true
        schema:
          type: integer
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Collections'
            application/xml:
              schema:
                $ref: '#/components/schemas/Collections'
        "400":
          description: Invalid city_id.
  /cuisines:
    get:
      tags:
      - Cuisines
      summary: Get a list of all cuisines of restaurants listed in a city.
      description: List of all restaurants serving a particular cuisine can be obtained
        using '/search' API with cuisine ID and location details.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: lat
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: lon
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: city_id
        in: query
        description: id of the city for which cuisines are needed
        required: false
        style: form
        explode: true
        schema:
          type: string
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Cuisines'
            application/xml:
              schema:
                $ref: '#/components/schemas/Cuisines'
        "403":
          description: Invalid Key.
  /establishments:
    get:
      tags:
      - Establishments
      summary: Get a list of restaurant types in a city.
      description: List of all restaurants categorized under a particular restaurant
        type can obtained using /Search API with Establishment ID and location details
        as inputs.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: lat
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: lon
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: city_id
        in: query
        description: id of the city
        required: false
        style: form
        explode: true
        schema:
          type: string
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Establishments'
            application/xml:
              schema:
                $ref: '#/components/schemas/Establishments'
        "403":
          description: Invalid API-Key.
  /geocode:
    get:
      tags:
      - Geocode
      summary: Get location details based on coordinates
      description: Get Foodie and Nightlife Index, list of popular cuisines and nearby
        restaurants around the given coordinates.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: lat
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: lon
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Geocode'
            application/xml:
              schema:
                $ref: '#/components/schemas/Geocode'
        "403":
          description: Invalid API-Key.
  /locations:
    get:
      tags:
      - Zomato Search
      summary: Search for locations.
      description: Search for Zomato locations by keyword. Provide coordinates to
        get better search results.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: query
        in: query
        description: suggestion for location name
        required: true
        style: form
        explode: true
        schema:
          type: integer
      - name: lat
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: lon
        in: query
        description: latitude / longitude of any point within a city
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: cunt
        in: query
        description: max number of results to fetch
        required: false
        style: form
        explode: true
        schema:
          type: integer
      responses:
        "200":
          description: Successful operation.
        "403":
          description: Invalid API-Key.
  /location_details:
    get:
      tags:
      - Zomato location
      summary: Get Zomato location details.
      description: Get Foodie Index, Nightlife Index, Top Cuisines and Best rated
        restaurants in a given location
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: entity_id
        in: query
        description: location id obtained from locations api
        required: true
        style: form
        explode: true
        schema:
          type: integer
      - name: entity_type
        in: query
        description: location type obtained from locations api
        required: true
        style: form
        explode: true
        schema:
          type: string
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Location'
            application/xml:
              schema:
                $ref: '#/components/schemas/Location'
        "403":
          description: Invalid API-Key.
  /restaurant:
    get:
      tags:
      - Restaurant
      summary: Get restaurant details.
      description: Get detailed restaurant information using Zomato restaurant ID.
        Partner Access is required to access photos and reviews.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: res_id
        in: query
        description: id of restaurant whose details are requested
        required: true
        style: form
        explode: true
        schema:
          type: integer
      responses:
        "200":
          description: Successful operation.
        "400":
          description: Invalid res_id.
  /dailymenu:
    get:
      tags:
      - Restaurant Dailymenu
      summary: Get daily menu of a restaurant
      description: Get daily menu using Zomato restaurant ID.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: res_id
        in: query
        description: id of restaurant whose details are requested
        required: true
        style: form
        explode: true
        schema:
          type: integer
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Menu'
            application/xml:
              schema:
                $ref: '#/components/schemas/Menu'
        "400":
          description: Invalid res_id.
  /reviews:
    get:
      tags:
      - Restaurant Reviews
      summary: Get restaurant reviews.
      description: Get restaurant reviews using the Zomato restaurant ID. Only 5 latest
        reviews are available under the Basic API plan.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: res_id
        in: query
        description: id of restaurant whose details are requested
        required: true
        style: form
        explode: true
        schema:
          type: integer
      - name: start
        in: query
        description: fetch results after this offset
        required: false
        style: form
        explode: true
        schema:
          type: integer
      - name: count
        in: query
        description: max number of results to retrieve
        required: false
        style: form
        explode: true
        schema:
          type: integer
      responses:
        "200":
          description: Successful operation.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Review'
            application/xml:
              schema:
                $ref: '#/components/schemas/Review'
        "400":
          description: Invalid res_id.
  /search:
    get:
      tags:
      - Restaurant Search
      summary: Search for restaurant
      description: The location input can be specified using Zomato location ID or
        coordinates. Cuisine / Establishment / Collection IDs can be obtained from
        respective api calls. Get up to 100 restaurants by changing the 'start' and
        'count' parameters with the maximum value of count being 20. Partner Access
        is required to access photos and reviews.
      parameters:
      - name: user-key
        in: header
        description: your API key
        required: true
        style: simple
        explode: false
        schema:
          type: string
      - name: entity_id
        in: query
        description: location id
        required: false
        style: form
        explode: true
        schema:
          type: integer
      - name: entity_type
        in: query
        description: location type
        required: false
        style: form
        explode: true
        schema:
          type: array
          items:
            type: string
            default: available
            enum:
            - city
            - subzone
            - zone
            - landmark
            - metro
            - group
      - name: q
        in: query
        description: query by city name
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: lat
        in: query
        description: latitude
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: lon
        in: query
        description: longitude
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: start
        in: query
        description: fetch results after this offset
        required: false
        style: form
        explode: true
        schema:
          type: integer
      - name: count
        in: query
        description: max number of results to retrieve
        required: false
        style: form
        explode: true
        schema:
          type: integer
      - name: cuisine
        in: query
        description: list of cuisine id's separated by comma
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: radius
        in: query
        description: radius around (lat,lon); to define search area, defined in meters(M)
        required: false
        style: form
        explode: true
        schema:
          type: number
      - name: establishment_type
        in: query
        description: estblishment id obtained from establishments call
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: collection_id
        in: query
        description: collection id obtained from collections call
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: category
        in: query
        description: category ids obtained from categories call
        required: false
        style: form
        explode: true
        schema:
          type: string
      - name: sort
        in: query
        description: sort restaurants by ..
        required: false
        style: form
        explode: true
        schema:
          type: array
          items:
            type: string
            default: available
            enum:
            - cost
            - rating
            - real_distance
      - name: order
        in: query
        description: used with 'sort' parameter to define ascending / descending
        required: false
        style: form
        explode: true
        schema:
          type: array
          items:
            type: string
            default: available
            enum:
            - asc
            - dsc
      responses:
        "200":
          description: Successful operation.
        "400":
          description: Failed.
components:
  schemas:
    Categories:
      type: object
      properties:
        category_id:
          type: integer
          format: int64
          example: 3
        category_name:
          type: string
          example: Dine-out
      xml:
        name: Tag
    Cities:
      type: object
      properties:
        id:
          type: integer
          format: int64
          example: 280
        name:
          type: string
          example: New York City, NY
        country_id:
          type: integer
          format: int64
          example: 216
        country_name:
          type: string
          example: United States
        is_state:
          type: boolean
          example: false
        state_id:
          type: integer
          format: int64
          example: 103
        state_name:
          type: string
          example: New York State
        state_code:
          type: string
          example: NY
    Collections:
      type: object
      properties:
        collection_id:
          type: integer
          format: int64
          example: 1
        title:
          type: string
          example: Trending this week
        url:
          type: string
          example: https://www.zomato.com/new-york-city/top-restaurants
        description:
          type: string
          example: The most popular restaurants in town this week
        image_url:
          type: string
          example: https://b.zmtcdn.com/data/collections/e40960514831cb9b74c552d69eceee0f_1418387628_l.jpg
        res_count:
          type: integer
          example: 30
        share_url:
          type: string
          example: http://www.zoma.to/c-280/1
    Cuisines:
      type: object
      properties:
        cuisine_id:
          type: integer
          example: 25
        cuisine_name:
          type: string
          example: string
    Establishments:
      type: object
      properties:
        establishment_id:
          type: integer
          example: 31
        establishment_name:
          type: string
          example: Bakery
    Location:
      type: object
      properties:
        entity_type:
          type: string
          example: group
        entity_id:
          type: integer
          example: 36932
        title:
          type: string
          example: Chelsea Market, Chelsea, New York City
        latitude:
          type: number
          example: 40.742051
        longitude:
          type: integer
        city_id:
          type: integer
          example: 280
        city_name:
          type: string
          example: New York City
        country_id:
          type: integer
          example: 216
        country_name:
          type: string
          example: United States
    Menu:
      type: object
      properties:
        daily_menu:
          $ref: '#/components/schemas/Menu_daily_menu'
    Review:
      type: object
      properties:
        rating:
          type: integer
        review_text:
          type: string
          example: The best latte I've ever had. It tasted a little sweet
        id:
          type: number
          example: 24127336
        rating_color:
          type: string
          example: 305D02
        review_time_friendly:
          type: string
          example: 2 months ago
        rating_text:
          type: string
          example: Insane!
        timestamp:
          type: number
          example: 1435507367
        likes:
          type: integer
          example: 0
        user:
          $ref: '#/components/schemas/Review_user'
        comments_count:
          type: integer
          example: 0
    Geocode:
      type: object
      properties:
        locality:
          $ref: '#/components/schemas/Geocode_locality'
        popularity:
          $ref: '#/components/schemas/Geocode_popularity'
        link:
          type: string
          example: https://www.zomato.com/new-york-city/chelsea-restaurants
        nearby_restaurants:
          $ref: '#/components/schemas/Geocode_nearby_restaurants'
    Menu_daily_menu_dishes:
      type: object
      properties:
        dish_id:
          type: integer
          example: 104089345
        name:
          type: string
          example: Tatarák ze sumce s toustem
        price:
          type: string
          example: 49 Kč
    Menu_daily_menu:
      type: object
      properties:
        daily_menu_id:
          type: integer
          example: 6507624
        name:
          type: string
          example: Vinohradský pivovar
        start_date:
          type: string
          example: 2016-03-08 11:00
        end_date:
          type: string
          example: 016-03-08 15:00
        dishes:
          $ref: '#/components/schemas/Menu_daily_menu_dishes'
    Review_user:
      type: object
      properties:
        name:
          type: string
          example: John Doe
        zomato_handle:
          type: string
          example: John
        foodie_level:
          type: string
          example: Super Foodie
        foodie_level_num:
          type: number
          example: 9
        foodie_color:
          type: string
          example: f58552
        profile_url:
          type: string
          example: https://www.zomato.com/john
        profile_deeplink:
          type: string
          example: zoma.to/u/1170245
        profile_image:
          type: string
          example: string
    Geocode_locality:
      type: object
      properties:
        entity_type:
          type: string
          example: group
        entity_id:
          type: integer
          example: 36932
        title:
          type: string
          example: Chelsea Market, Chelsea, New York City
        latitude:
          type: number
          example: 40.742051
        longitude:
          type: number
          example: -74.004821
        city_id:
          type: integer
          example: 280
        city_name:
          type: string
          example: New York City
        country_id:
          type: integer
          example: 216
        country_name:
          type: string
          example: United States
    Geocode_popularity:
      type: object
      properties:
        popularity:
          type: number
          example: 4.92
        nightlife_index:
          type: number
          example: 4.95
        top_cuisines:
          type: string
          example: cafe
    Geocode_nearby_restaurants_location:
      type: object
      properties:
        address:
          type: string
          example: 15th Avenue, New York, NY 10003
        locality:
          type: string
          example: Greenwich Village
        city:
          type: string
          example: New York City
        latitude:
          type: number
          example: 40.73201
        longitude:
          type: number
          example: -73.996155
        zipcode:
          type: integer
          example: 10003
        country_id:
          type: integer
          example: 216
    Geocode_nearby_restaurants_user_rating:
      type: object
      properties:
        aggregate_rating:
          type: number
          example: 3.7
        rating_text:
          type: string
          example: Very Good
        rating_color:
          type: string
          example: 5BA829
        votes:
          type: number
          example: 1046
    Geocode_nearby_restaurants_photos:
      type: object
      properties:
        id:
          type: string
          example: u_MjA5MjY1OTk5OT
        url:
          type: string
          example: https://b.zmtcdn.com/data/reviews_photos/c15/9eb13ceaf6e90129c276ce6ff980bc15_1435111695_640_640_thumb.JPG
        thumb_url:
          type: string
          example: https://b.zmtcdn.com/data/reviews_photos/c15/9eb13ceaf6e90129c276ce6ff980bc15_1435111695_200_thumb.JPG
        user:
          $ref: '#/components/schemas/Review_user'
    Geocode_nearby_restaurants:
      type: object
      properties:
        id:
          type: number
          example: 16774318
        name:
          type: string
          example: Otto Enoteca & Pizzeria
        url:
          type: string
          example: https://www.zomato.com/new-york-city/otto-enoteca-pizzeria-greenwich-village
        location:
          $ref: '#/components/schemas/Geocode_nearby_restaurants_location'
        average_cost_for_two:
          type: number
          example: 60
        price_range:
          type: number
          example: 2
        currency:
          type: string
          example: $
        thumb:
          type: string
          example: https://b.zmtcdn.com/data/pictures/chains/8/16774318/a54deb9e4dbb79dd7c8091b30c642077_featured_thumb.png
        featured_image:
          type: string
          example: https://d.zmtcdn.com/data/pictures/chains/8/16774318/a54deb9e4dbb79dd7c8091b30c642077_featured_v2.png
        photos_url:
          type: string
          example: https://www.zomato.com/new-york-city/otto-enoteca-pizzeria-greenwich-village/photos#tabtop
        menu_url:
          type: string
          example: https://www.zomato.com/new-york-city/otto-enoteca-pizzeria-greenwich-village/menu#tabtop
        events_url:
          type: string
          example: https://www.zomato.com/new-york-city/otto-enoteca-pizzeria-greenwich-village/menu#tabtop
        user_rating:
          $ref: '#/components/schemas/Geocode_nearby_restaurants_user_rating'
        has_online_delivery:
          type: integer
          example: 0
        is_delivering_now:
          type: integer
          example: 0
        has_table_booking:
          type: integer
          example: 0
        deeplink:
          type: string
          example: zomato://r/16774318
        cuisines:
          type: string
          example: cafe
        all_reviews_count:
          type: integer
          example: 15
        photos_count:
          type: integer
          example: 18
        phone_numbers:
          type: number
        photos:
          $ref: '#/components/schemas/Geocode_nearby_restaurants_photos'