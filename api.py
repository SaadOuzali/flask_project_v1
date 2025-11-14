from flask import Flask, jsonify, request
from mysql.connector import Error
from db import MysqlConnector
from helpers import db_config, init_db
from blogs import Blog
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


# Home route
@app.route("/")
def home():
    return jsonify({"message": "Flask API is running!"})


# get all blogs
@app.route("/api/blog", methods=["GET"])
def get_all_blogs():
    try:
        blogs = Blog.get_all_blogs()
        return jsonify({"status": "success", "blogs": blogs}), 200
    except Error as e:
       return jsonify({"status": "faillure", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "faillure", "msg": "internal prb"}), 500


# create blog
@app.route("/api/blog", methods=["POST"])
def create_blog():
    try:
        body = request.json
        create_blog = Blog(title=body["title"], content=body["content"]).save()
        return jsonify({"status": "success", "blog_id": create_blog}), 201
    except Error as e:
        return jsonify({"status": "faillure", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "faillure", "msg": "internal prb"}), 500


# update blog
@app.route("/api/blog/<int:blog_id>", methods=["PUT"])
def update_blog(blog_id):

    try:
        body = request.json
        is_updated_blog = Blog(
            id=blog_id, title=body["title"], content=body["content"]
        ).update()

        if is_updated_blog:
            return jsonify({"message": "blog updated successfully"}), 200
        else:
            return jsonify({"message": "invalid blog id "}), 400
    except Error as e:
        return jsonify({"status": "faillure", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "faillure", "msg": "internal prb"}), 500


# delete blog
@app.route("/users/<int:blog_id>", methods=["DELETE"])
def delete_blog(blog_id):
    try:
        is_deleted_blog = Blog(id=blog_id)

        if is_deleted_blog:
            return jsonify({"message": "blog deleted successfully"}), 200
        else:
            return jsonify({"message": "invalid blog id "}), 400
    except Error as e:
        return jsonify({"status": "faillure", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "faillure", "msg": "internal prb"}), 500


#translate blog
@app.route("/api/blog/<int:blog_id>", methods=["GET"])
def translate_blog(blog_id):
    
    source = request.args.get("source")
    target = request.args.get("target")
    
    if not source:
        return jsonify({"status": "error", "message": "source is required"}), 400
    if not target:
        return jsonify({"status": "error", "message": "target is required"}), 400
    try:
        
        blog, is_find_blog = Blog(id=blog_id).get_by_Id()
        print("d5al hna")
        if is_find_blog and blog:

            translated_blog = blog.translate(source_lang=source, target_lang=target)
            return (
                jsonify(
                    {
                        "message": "blog translated successfully",
                        "data": {
                            "original_blog": blog.content,
                            "translated_content": translated_blog,
                        },
                    }
                ),
                200,
            )
        
       
        else:
            return jsonify({"message": "invalid blog id "}), 404
    except Error as e:
        return jsonify({"status": "faillure", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "faillure", "msg": "internal prb"}), 500
    


#translate the blog and generate the audio
@app.route("/api/blog/generate/<int:blog_id>", methods=["GET"])
def translate_and_generate_audio_of_blog(blog_id):
    
    source = request.args.get("source")
    target = request.args.get("target")
    
    if not source:
        return jsonify({"status": "error", "message": "source is required"}), 400
    if not target:
        return jsonify({"status": "error", "message": "target is required"}), 400
    try:
        
        blog, is_find_blog = Blog(id=blog_id).get_by_Id()
        
        if is_find_blog and blog:

            translated_blog = blog.translate_and_generate_audio(source_lang=source, target_lang=target)
            print(f"translated  {translated_blog}")
            return (
                jsonify(
                    {
                        "message": "blog translated successfully and audio generated for it",
                        "data": {
                            "original_blog": blog.content,
                            "translated_content": translated_blog
                        },
                    }
                ),
                200,
            )
        
       
        else:
            return jsonify({"message": "invalid blog id "}), 404
    except Error as e:
        return jsonify({"status": "faillure", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "faillure", "msg": "internal prb"}), 500


if __name__ == "__main__":

    app.run(debug=True)
