# Color Palettes API

This API manages color palettes. <br>
Developers can easily save, organize, and retrieve color schemes to streamline the design process.
- Flask
- MongoDB connection
- vercel Deployment
  
## Endpoints
### *1️⃣ Create a New Color Palette*
POST /color-palette <br>
Description: Create a new color palette
Request Body:
```java
{
  "colorsList": [
    "string"
  ],
  "description": "string",
  "name": "string",
  "package_name": "string"
}
```
Responses:
- *201*: Color palette created successfully.
- *400*: Invalid request or date format.
- *400*: Palette name alredy exists.
- *500*: Database connection error.

### *2️⃣ Get palette names for package name*
GET /color-palette/<package_name> <br>
Description: Get all colors palette names and description <br>
Path Parameters:
```java
- package_name (string)
```
Responses:
- *200*: List of palettes info (name and description).
- *404*: No color palette names found.
- *500*: Database connection error.

 ### *3️⃣ Get a color palette by name*
GET /color-palette/<package_name>/<palette_name> <br>
Description: Get details of a specific color palette by name <br>
Path Parameters:
```java
- package_name (string)
- name (string) : name of palette
```
Responses:
- *200*: color palette
- *404*: No color palette found.
- *500*: Database connection error.


## 🤝 Contributing
Feel free to open issues or contribute via pull requests. Feedback is always welcome!

## 📜 License
This project is licensed under the *MIT License*.

---
📌 *Maintained by:*  Noa Sharabi 
