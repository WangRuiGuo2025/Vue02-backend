from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from sqlite3 import Error

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class message(BaseModel):
    name:str;
    email:str;
    message:str;

class reply(BaseModel):
    name:str;
    email:str;
    message:str;
    mid:int;

class Good(BaseModel):
    id:int;
    good:int;

class Bad(BaseModel):
    id:int;
    bad:int;

DB_PATH = "message_board.db"

def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(f"数据库连接失败：{e}")
    return conn

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/message")
async def sendMessage(data:message):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        insert_sql = """
        INSERT INTO message_table (name, mid, email, message, timestamp)
        VALUES (?, 0, ?, ?, CURRENT_TIMESTAMP);
        """
        cursor.execute(insert_sql, (data.name, data.email, data.message))
        conn.commit()

        return {"message": "OK", "detail": f"留言ID：{cursor.lastrowid} 保存成功"}

    except Error as e:
        return {"message": "Failed", "error": str(e)}
    finally:
        if conn:
            conn.close()

@app.post("/reply")
async def sendReply(data:reply):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        insert_sql = """
        INSERT INTO message_table (name, mid, email, message, timestamp)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP);
        """
        cursor.execute(insert_sql, (data.name,data.mid, data.email, data.message))
        conn.commit()

        return {"message": "OK", "detail": f"回复ID：{cursor.lastrowid} 保存成功"}

    except Error as e:
        return {"message": "Failed", "error": str(e)}
    finally:
        if conn:
            conn.close()
@app.get("/number")
async def number():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM message_table ORDER BY id ASC")
        rows = cursor.fetchall()
        result = []
        max_id = 0
        for row in rows:
            result.append({
                "id": row["id"],
           })
        for item in result:
            current_id = item["id"]
            if current_id > max_id:
                max_id = current_id
        return {    
            "code": 200,
            "message": "success",
            "data": max_id
        }
    except Error as e:
        return {
            "code": 500,
            "message": "failed",
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()

@app.get("/list")
async def getMessage():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM message_table ORDER BY id ASC")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "name": row["name"],
                "mid": row["mid"],
                "email": row["email"],
                "message": row["message"],
                "good": row["good"],
                "bad": row["bad"],
                "timestamp": row["timestamp"]
            })

        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Error as e:
        return {
            "code": 500,
            "message": "failed",
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()

@app.post("/update-good")
async def update_good(data: Good):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM message_table WHERE id = ?", (data.id,))
        if not cursor.fetchone():
            return {
                "code": 404,
                "message": "failed",
                "error": f"ID为{data.id}的留言不存在"
            }

        update_sql = """
        UPDATE message_table
        SET good = ?
        WHERE id = ?;
        """
        cursor.execute(update_sql, (data.good, data.id))
        conn.commit()

        return {
            "code": 200,
            "message": "success",
            "detail": f"ID为{data.id}的留言点赞数已更新为{data.good}"
        }

    except Error as e:
        return {
            "code": 500,
            "message": "failed",
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()

@app.post("/update-bad")
async def update_bad(data: Bad):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM message_table WHERE id = ?", (data.id,))
        if not cursor.fetchone():
            return {
                "code": 404,
                "message": "failed",
                "error": f"ID为{data.id}的留言不存在"
            }

        update_sql = """
        UPDATE message_table
        SET bad = ?
        WHERE id = ?;
        """
        cursor.execute(update_sql, (data.bad, data.id))
        conn.commit()

        return {
            "code": 200,
            "message": "success",
            "detail": f"ID为{data.id}的留言点踩数已更新为{data.bad}"
        }

    except Error as e:
        return {
            "code": 500,
            "message": "failed",
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()