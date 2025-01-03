user_login_dict = {
  "tags": [
    "Authentication"
  ],
  "definitions": {
    "UserLoginData": {
      "type": "object",
          "properties": {
            "email": {
              "type": "string"
            },
            "password": {
              "type": "string"
            }
          }
    }
  },
  "parameters": [
    {
      "name": "Login",
      "in": "body",
      "description": "User login",
      "required": True,
      "schema": {
        "$ref": "#/definitions/UserLoginData"
      },
    }
  ],
  "responses": {
    "200": {
      "description": "User successfully logged in"
    },
    "400": {
      "description": "Invalid request"
    },
    "401": {
      "description": "Not authorized"
    },
    "500": {
      "description": "An internal error occurred"
    }
  }
}

register_user_dict = {
  "tags": [
    "Authentication"
  ],
  "definitions": {
    "RegisterUserData": {
      "type": "object",
          "properties": {
            "email": {
              "type": "string"
            },
            "password": {
              "type": "string"
            },
            "strava_id": {
              "type": "integer"
            }
          }
    }
  },
  "parameters": [
    {
      "name": "Register",
      "in": "body",
      "description": "Register a new user",
      "required": True,
      "schema": {
        "$ref": "#/definitions/RegisterUserData"
      },
    }
  ],
  "responses": {
    "201": {
      "description": "User successfully registered"
    },
    "400": {
      "description": "Invalid request"
    },
    "409": {
      "description": "User already exists"
    },
    "500": {
      "description": "An internal error occurred"
    }
  }
}

add_athlete_dict = {
  "tags": [
    "Athletes"
  ],
  "parameters": [
    {
      "name": "Athlete data",
      "in": "body",
      "description": "Athlete Strava profile data",
      "required": True,
      "schema": {
        "$ref": "#/definitions/AthleteData"
      },
    }
  ],
  "definitions": {
    "AthleteData": {
      "type": "object",
          "properties": {
            "strava_id": {
              "type": "string"
            },
            "username": {
              "type": "string"
            },
            "firstname": {
              "type": "string"
            },
            "lastname": {
              "type": "string"
            },
            "email": {
              "type": "string"
            },
            "city": {
              "type": "string"
            },
            "country": {
              "type": "string"
            },
            "sex": {
              "type": "string"
            },
            "weight": {
              "type": "string"
            },
            "profile": {
              "type": "string"
            },
            "created_at": {
              "type": "string"
            }
          }
    }
  },
  "responses": {
    "201": {
      "description": "Athlete added"
    },
    "400": {
      "description": "Invalid request"
    }
  }
}

get_athlete_dict = {
  "tags": [
    "Athletes"
  ],
  "parameters": [
    {
      "name": "Athlete ID",
      "in": "path",
      "description": "Strava Stats athlete id",
      "required": True,
    }
  ],
  "responses": {
    "200": {
      "description": "Athlete found",
      "schema": {
        "$ref": "#/definitions/AthleteData"
      }
    },
    "400": {
      "description": "Error, athlete not found"
    }
  }
}


add_activity_dict = {
  "tags": [
    "Activities"
  ],
  "parameters": [
    {
      "name": "Activity data",
      "in": "body",
      "description": "Activity data mapping to Strava data fields",
      "required": True,
      "schema": {
        "$ref": "#/definitions/ActivityData"
      },
    }
  ],
  "definitions": {
    "ActivityData": {
      "type": "object",
          "properties": {
            "athlete_id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "description": {
              "type": "string"
            },
            "distance": {
              "type": "integer"
            },
            "moving_time": {
              "type": "integer"
            },
            "elapsed_time": {
              "type": "integer"
            },
            "start_date": {
              "type": "integer"
            },
            "start_latitude": {
              "type": "float"
            },
            "start_longitude": {
              "type": "float"
            },
            "achievement_count": {
              "type": "integer"
            },
            "kudos_count": {
              "type": "integer"
            },
            "comment_count": {
              "type": "integer"
            },
            "photo_count": {
              "type": "integer"
            },
            "pr_count": {
              "type": "integer"
            },
            "calories": {
              "type": "integer"
            },
            "average_speed": {
              "type": "float"
            },
            "max_speed": {
              "type": "float"
            },
            "average_watts": {
              "type": "float"
            },
            "average_temp": {
              "type": "float"
            },
            "elevation_gain": {
              "type": "integer"
            },
            "bikepacking": {
              "type": "integer"
            }
          }
    }
  },
  "responses": {
    "201": {
      "description": "Activity added"
    },
    "400": {
        "description": "Invalid request"
      }
  }
}

get_activities_dict = {
  "tags": [
    "Activities"
  ],
  "parameters": [
    {
      "name": "Athlete ID",
      "in": "path",
      "description": "Strava athlete id",
      "required": True,
    }
  ],
  "responses": {
    "200": {
      "description": "Athlete found",
      "schema": {
        "$ref": "#/definitions/ActivityData"
      }
    },
    "500": {
      "description": "An internal error occurred"
    }
  }
}

add_gear_dict = {
  "tags": [
    "Gears"
  ],
   "definitions": {
    "GearData": {
      "type": "object",
          "properties": {
            "strava_gear_id": {
              "type": "string"
            },
            "name": {
              "type": "string"
            },
            "brand_name": {
              "type": "string"
            },
            "model_name": {
              "type": "string"
            },
            "description": {
              "type": "string"
            },
            "primary": {
              "type": "integer"
            },
            "retired": {
              "type": "integer"
            },
            "weight": {
              "type": "integer"
            },
            "created_at": {
              "type": "integer"
            },
          }
    }
   },
  "parameters": [
    {
      "name": "Gear data",
      "in": "body",
      "description": "Bike attributes",
      "required": True,
      "schema": {
        "$ref": "#/definitions/GearData"
      },
    }
  ],
  "responses": {
    "201": {
      "description": "Gear added"
    },
    "400": {
        "description": "Invalid request"
      }
  }
}

get_gears_dict = {
  "tags": [
    "Gears"
  ],
  "responses": {
    "200": {
      "description": "List of of all bikes",
      "schema": {
        "$ref": "#/definitions/GearData"
      }
    },
    "500": {
      "description": "An internal error occurred"
    }
  }
}
