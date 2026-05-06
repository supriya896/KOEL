
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from config import Config
from sqlalchemy import or_
from models import Document, db, VehicleTypeMaster, VehicleTypeDetails,DockInOutDetails,TripStatus, MasterVehicle, MasterDriver,DocumentSummaryView,DockSummaryView
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

app.config['JSON_SORT_KEYS'] = False



from sqlalchemy import text
from datetime import date


# @app.route("/api/document-summary", methods=["GET"])

# def get_document_summary():

#     try:

#         query = text("""

#             SELECT 

#                 trip_id,

#                 gate_exit_status,

#                 timestamp,

#                 loading_or_unloading,

#                 vehicle_number,

#                 green_channel,

#                 gate_entry_number

#             FROM document_summary_view

#         """)

#         result = db.session.execute(query).fetchall()

#         data = [

#             {

#                 "trip_id": row[0],

#                 "gate_exit_status": row[1],

#                 "timestamp": row[2],

#                 "loading_or_unloading": row[3],

#                 "vehicle_number": row[4],

#                 "green_channel": row[5],

#                 "gate_entry_number": row[6],

#             }

#             for row in result

#         ]

#         return jsonify({

#             "success": True,

#             "count": len(data),

#             "data": data

#         }), 200

#     except Exception as e:

#         return jsonify({

#             "success": False,

#             "error": str(e)

#         }), 500
        
        

           
              
# ===================== PRAVESH API =====================
# @app.route("/api/pravesh", methods=["GET"])
# def pravesh_api():
#     try:
#         today = date.today()
#         card_type = request.args.get("type")

#         # Queries
#         total_in_query = text("""
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date
#         """)
#         total_out_query = text("""
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date AND gate_exit_status = 'EXITED'
#         """)
#         inside_query = text("""
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date AND gate_exit_status IS NULL
#         """)

#         columns = ["vehicle_number", "trip_id", "timestamp", "gate_entry_number",
#                    "loading_or_unloading", "green_channel", "gate_exit_status"]

#         # Return detail data if a specific card type is requested
#         if card_type == "total_in":
#             result = db.session.execute(total_in_query, {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200
#         elif card_type == "total_out":
#             result = db.session.execute(total_out_query, {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200
#         elif card_type == "inside":
#             result = db.session.execute(inside_query, {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         # Otherwise return summary counts
#         total_in = db.session.execute(total_in_query, {"today_date": today}).fetchall()
#         total_out = db.session.execute(total_out_query, {"today_date": today}).fetchall()
#         inside = db.session.execute(inside_query, {"today_date": today}).fetchall()

#         return jsonify({
#             "success": True,
#             "counts": {
#                 "total_in": len(total_in),
#                 "total_out": len(total_out),
#                 "inside": len(inside)
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500


# Helper to add load_type filter to a query
def apply_load_type_filter(query, load_type, column_name="loading_or_unloading"):
    if load_type == "loading":
        return query + f" AND {column_name} = 'Loading'"
    elif load_type == "unloading":
        return query + f" AND {column_name} = 'Unloading'"
    return query

# # ===================== PRAVESH API =====================
# @app.route("/api/pravesh", methods=["GET"])
# def pravesh_api():
#     try:
#         today = date.today()
#         card_type = request.args.get("type")
#         load_type = request.args.get("load_type")  # 'loading', 'unloading', or None

#         # Base query (without exit status filter)
#         base_query = """
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date
#         """
#                 # Base query for HOLD vehicles (previous days, still inside)
#         hold_base_query = """
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status
#             FROM document_summary_view
#             WHERE gate_exit_status IS NULL
#             AND DATE(timestamp) < :today_date
#         """
        
#         # Apply load_type filter if provided (for detail queries)
#         if load_type in ('loading', 'unloading'):
#             base_query = apply_load_type_filter(base_query, load_type)

#         columns = ["vehicle_number", "trip_id", "timestamp", "gate_entry_number",
#                    "loading_or_unloading", "green_channel", "gate_exit_status"]

#         # Detail responses
#         if card_type == "total_in":
#             query = base_query + " ORDER BY timestamp ASC"
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200
#         elif card_type == "total_out":
#             query = base_query + " AND gate_exit_status = 'EXITED' ORDER BY timestamp ASC"
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200
#         elif card_type == "inside":
#             query = base_query + " AND gate_exit_status IS NULL ORDER BY timestamp ASC"
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200
#         elif card_type == "vehicle_hold":
#             query = hold_base_query
#             if load_type in ('loading', 'unloading'):
#                 query = apply_load_type_filter(query, load_type)
#             query += " ORDER BY timestamp ASC"
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         # --- Summary counts (split by loading/unloading) ---
#         def get_count(base_sql, load_type_val=None):
#             sql = base_sql
#             if load_type_val in ('loading', 'unloading'):
#                 sql = apply_load_type_filter(sql, load_type_val)
#             result = db.session.execute(text(sql), {"today_date": today}).fetchall()
#             return len(result)

#         # total_in (no extra filter)
#         total_in_loading = get_count(base_query, "loading")
#         total_in_unloading = get_count(base_query, "unloading")

#         # total_out (with gate_exit_status = 'EXITED')
#         out_query = base_query + " AND gate_exit_status = 'EXITED'"
#         total_out_loading = get_count(out_query, "loading")
#         total_out_unloading = get_count(out_query, "unloading")

#         # inside (gate_exit_status IS NULL)
#         inside_query = base_query + " AND gate_exit_status IS NULL"
#         inside_loading = get_count(inside_query, "loading")
#         inside_unloading = get_count(inside_query, "unloading")
        
#          # vehicle_hold counts (previous days, still inside)
#         hold_loading = get_count(hold_base_query, "loading")
#         hold_unloading = get_count(hold_base_query, "unloading")

#         return jsonify({
#             "success": True,
#             "counts": {
#                 "total_in": {
#                     "loading": total_in_loading,
#                     "unloading": total_in_unloading,
#                     "total": total_in_loading + total_in_unloading
#                 },
#                 "total_out": {
#                     "loading": total_out_loading,
#                     "unloading": total_out_unloading,
#                     "total": total_out_loading + total_out_unloading
#                 },
#                 "inside": {
#                     "loading": inside_loading,
#                     "unloading": inside_unloading,
#                     "total": inside_loading + inside_unloading
#                 },
#                 "vehicle_hold": {
#                     "loading": hold_loading,
#                     "unloading": hold_unloading,
#                     "total": hold_loading + hold_unloading
#                 }
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# ===================== PRAVESH API =====================
@app.route("/api/pravesh", methods=["GET"])
def pravesh_api():
    try:
        today = date.today()
        card_type = request.args.get("type")
        load_type = request.args.get("load_type")  # 'loading', 'unloading', or None

        # Base query (without exit status filter)
        base_query = """
            SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
                   loading_or_unloading, green_channel, gate_exit_status,
                   gate_exit_time,
                   CASE 
                       WHEN gate_exit_status = 'EXITED' THEN 
                           CONCAT(
                               FLOOR(EXTRACT(EPOCH FROM (gate_exit_time - timestamp)) / 3600), ' h ',
                               FLOOR((EXTRACT(EPOCH FROM (gate_exit_time - timestamp)) % 3600) / 60), ' m'
                           )
                       ELSE 
                           CONCAT(
                               FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - timestamp)) / 3600), ' h ',
                               FLOOR((EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - timestamp)) % 3600) / 60), ' m'
                           )
                   END as duration
            FROM (
                SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
                       loading_or_unloading, green_channel, gate_exit_status,
                       MAX(CASE WHEN location = 'GATE EXIT' THEN time END) 
                           OVER (PARTITION BY trip_id) as gate_exit_time,
                       ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY timestamp) as rn
                FROM document_summary_view_dummy
                WHERE DATE(timestamp) = :today_date
            ) sub
            WHERE rn = 1
        """
        
        # Base query for HOLD vehicles (previous days, still inside)
        hold_base_query = """
            SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
                   loading_or_unloading, green_channel, gate_exit_status,
                   gate_exit_time,
                   CONCAT(
                       FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - timestamp)) / 3600), ' h ',
                       FLOOR((EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - timestamp)) % 3600) / 60), ' m'
                   ) as duration
            FROM (
                SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
                       loading_or_unloading, green_channel, gate_exit_status,
                       MAX(CASE WHEN location = 'GATE EXIT' THEN time END) 
                           OVER (PARTITION BY trip_id) as gate_exit_time,
                       ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY timestamp) as rn
                FROM document_summary_view_dummy
                WHERE gate_exit_status IS NULL
                AND DATE(timestamp) < :today_date
            ) sub
            WHERE rn = 1
        """
        
        # Apply load_type filter if provided (for detail queries)
        if load_type in ('loading', 'unloading'):
            base_query = apply_load_type_filter(base_query, load_type)

        columns = ["vehicle_number", "trip_id", "timestamp", "gate_entry_number",
                   "loading_or_unloading", "green_channel", "gate_exit_status", 
                   "gate_exit_time", "duration"]

        # Detail responses
        if card_type == "total_in":
            query = base_query + " ORDER BY timestamp ASC"
            result = db.session.execute(text(query), {"today_date": today}).fetchall()
            data = [list(row) for row in result]
            return jsonify({"success": True, "columns": columns, "data": data}), 200
        elif card_type == "total_out":
            query = base_query + " AND gate_exit_status = 'EXITED' ORDER BY timestamp ASC"
            result = db.session.execute(text(query), {"today_date": today}).fetchall()
            data = [list(row) for row in result]
            return jsonify({"success": True, "columns": columns, "data": data}), 200
        elif card_type == "inside":
            query = base_query + " AND gate_exit_status IS NULL ORDER BY timestamp ASC"
            result = db.session.execute(text(query), {"today_date": today}).fetchall()
            data = [list(row) for row in result]
            return jsonify({"success": True, "columns": columns, "data": data}), 200
        elif card_type == "vehicle_hold":
            query = hold_base_query
            if load_type in ('loading', 'unloading'):
                query = apply_load_type_filter(query, load_type)
            query += " ORDER BY timestamp ASC"
            result = db.session.execute(text(query), {"today_date": today}).fetchall()
            data = [list(row) for row in result]
            return jsonify({"success": True, "columns": columns, "data": data}), 200

        # --- Summary counts (split by loading/unloading) ---
        def get_count(base_sql, load_type_val=None):
            sql = base_sql
            if load_type_val in ('loading', 'unloading'):
                sql = apply_load_type_filter(sql, load_type_val)
            result = db.session.execute(text(sql), {"today_date": today}).fetchall()
            return len(result)

        # total_in (no extra filter)
        total_in_loading = get_count(base_query, "loading")
        total_in_unloading = get_count(base_query, "unloading")

        # total_out (with gate_exit_status = 'EXITED')
        out_query = base_query + " AND gate_exit_status = 'EXITED'"
        total_out_loading = get_count(out_query, "loading")
        total_out_unloading = get_count(out_query, "unloading")

        # inside (gate_exit_status IS NULL)
        inside_query = base_query + " AND gate_exit_status IS NULL"
        inside_loading = get_count(inside_query, "loading")
        inside_unloading = get_count(inside_query, "unloading")
        
        # vehicle_hold counts (previous days, still inside)
        hold_loading = get_count(hold_base_query, "loading")
        hold_unloading = get_count(hold_base_query, "unloading")

        return jsonify({
            "success": True,
            "counts": {
                "total_in": {
                    "loading": total_in_loading,
                    "unloading": total_in_unloading,
                    "total": total_in_loading + total_in_unloading
                },
                "total_out": {
                    "loading": total_out_loading,
                    "unloading": total_out_unloading,
                    "total": total_out_loading + total_out_unloading
                },
                "inside": {
                    "loading": inside_loading,
                    "unloading": inside_unloading,
                    "total": inside_loading + inside_unloading
                },
                "vehicle_hold": {
                    "loading": hold_loading,
                    "unloading": hold_unloading,
                    "total": hold_loading + hold_unloading
                }
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# # ===================== GATE API =====================
# @app.route("/api/gate", methods=["GET"])
# def gate_api():
#     try:
#         today = date.today()
#         card_type = request.args.get("type")
#         load_type = request.args.get("load_type")

# # Gate In: gate_entry_number IS NOT NULL (no status filter)
#         gate_in_base = """
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status, gate_entry_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date AND gate_entry_number IS NOT NULL
#         """
#         # Gate Out: gate_entry_status = 'Close'
#         gate_out_base = """
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status, gate_entry_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date AND gate_entry_status = 'Close'
#         """

#         columns = ["vehicle_number", "trip_id", "timestamp", "gate_entry_number",
#                    "loading_or_unloading", "green_channel", "gate_exit_status", "gate_entry_status"]

#         # Detail responses
#         if card_type == "gate_in":
#             query = apply_load_type_filter(gate_in_base, load_type)
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200
#         elif card_type == "gate_out":
#             query = apply_load_type_filter(gate_out_base, load_type)
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         # Summary counts (split)
#         def get_count(base_sql, load_type_val=None):
#             sql = base_sql
#             if load_type_val in ('loading', 'unloading'):
#                 sql = apply_load_type_filter(sql, load_type_val)
#             result = db.session.execute(text(sql), {"today_date": today}).fetchall()
#             return len(result)

#         gate_in_loading = get_count(gate_in_base, "loading")
#         gate_in_unloading = get_count(gate_in_base, "unloading")
#         gate_out_loading = get_count(gate_out_base, "loading")
#         gate_out_unloading = get_count(gate_out_base, "unloading")

#         return jsonify({
#             "success": True,
#             "counts": {
#                 "gate_in": {
#                     "loading": gate_in_loading,
#                     "unloading": gate_in_unloading,
#                     "total": gate_in_loading + gate_in_unloading
#                 },
#                 "gate_out": {
#                     "loading": gate_out_loading,
#                     "unloading": gate_out_unloading,
#                     "total": gate_out_loading + gate_out_unloading
#                 }
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @app.route("/api/gate", methods=["GET"])
# def gate_api():
#     try:
#         today = date.today()
#         card_type = request.args.get("type")
#         load_type = request.args.get("load_type")

#         # ---------- Base queries (existing) ----------
#         # Gate In: gate_entry_number IS NOT NULL
#         gate_in_base = """
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number, 
#                    loading_or_unloading, green_channel, gate_exit_status, gate_entry_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date AND gate_entry_number IS NOT NULL
#         """
#         # Gate Out: gate_entry_status = 'Close'
#         gate_out_base = """
#             SELECT vehicle_number, trip_id, timestamp, gate_entry_number,
#                    loading_or_unloading, green_channel, gate_exit_status, gate_entry_status
#             FROM document_summary_view
#             WHERE DATE(timestamp) = :today_date AND gate_entry_status = 'Close'
#         """

#         # ---------- New base for gate_dock_pending ----------
#         # Vehicles with gate entry done but NO record in dock_summary_view
#         gate_dock_pending_base = """
#             SELECT dsv.vehicle_number, dsv.trip_id, dsv.timestamp, dsv.gate_entry_number,
#                    dsv.loading_or_unloading, dsv.green_channel, dsv.gate_exit_status, dsv.gate_entry_status
#             FROM document_summary_view dsv
#             LEFT JOIN dock_summary_view dkv ON dsv.trip_id = dkv.trip_id
#             WHERE DATE(dsv.timestamp) = :today_date
#               AND dsv.gate_entry_number IS NOT NULL
#               AND dkv.trip_id IS NULL
#         """

#         columns = ["vehicle_number", "trip_id", "timestamp", "gate_entry_number",
#                    "loading_or_unloading", "green_channel", "gate_exit_status", "gate_entry_status"]

#         # ---------- Detail responses ----------
#         if card_type == "gate_in":
#             query = apply_load_type_filter(gate_in_base, load_type) + " ORDER BY timestamp ASC"
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         elif card_type == "gate_out":
#             query = apply_load_type_filter(gate_out_base, load_type) + " ORDER BY timestamp ASC"
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         elif card_type == "gate_dock_pending":
#             query = apply_load_type_filter(gate_dock_pending_base, load_type)  + " ORDER BY timestamp ASC"
#             result = db.session.execute(text(query), {"today_date": today}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         # ---------- Summary counts (existing + new) ----------
#         def get_count(base_sql, load_type_val=None):
#             sql = base_sql
#             if load_type_val in ('loading', 'unloading'):
#                 sql = apply_load_type_filter(sql, load_type_val)
#             result = db.session.execute(text(sql), {"today_date": today}).fetchall()
#             return len(result)

#         # Existing counts
#         gate_in_loading = get_count(gate_in_base, "loading")
#         gate_in_unloading = get_count(gate_in_base, "unloading")
#         gate_out_loading = get_count(gate_out_base, "loading")
#         gate_out_unloading = get_count(gate_out_base, "unloading")

#         # New counts for gate_dock_pending
#         gate_dock_pending_loading = get_count(gate_dock_pending_base, "loading")
#         gate_dock_pending_unloading = get_count(gate_dock_pending_base, "unloading")

#         return jsonify({
#             "success": True,
#             "counts": {
#                 "gate_in": {
#                     "loading": gate_in_loading,
#                     "unloading": gate_in_unloading,
#                     "total": gate_in_loading + gate_in_unloading
#                 },
#                 "gate_out": {
#                     "loading": gate_out_loading,
#                     "unloading": gate_out_unloading,
#                     "total": gate_out_loading + gate_out_unloading
#                 },
#                 "gate_dock_pending": {
#                     "loading": gate_dock_pending_loading,
#                     "unloading": gate_dock_pending_unloading,
#                     "total": gate_dock_pending_loading + gate_dock_pending_unloading
#                 }
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/gate", methods=["GET"])
def gate_api():
    try:
        today = date.today()
        card_type = request.args.get("type")
        load_type = request.args.get("load_type")

        # Base query with type casting for gate_entry_in_time
        base_query = """
            SELECT vehicle_number, trip_id, timestamp, gate_entry_number, gate_entry_in_time,
                   loading_or_unloading, green_channel, gate_exit_status, gate_entry_status,
                   gate_exit_time,
                   CASE 
                       WHEN gate_exit_status = 'EXITED' AND gate_exit_time IS NOT NULL THEN 
                           CONCAT(
                               FLOOR(EXTRACT(EPOCH FROM (gate_exit_time - TO_TIMESTAMP(gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) / 3600), ' h ',
                               FLOOR((EXTRACT(EPOCH FROM (gate_exit_time - TO_TIMESTAMP(gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) % 3600) / 60), ' m'
                           )
                       ELSE 
                           CONCAT(
                               FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - TO_TIMESTAMP(gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) / 3600), ' h ',
                               FLOOR((EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - TO_TIMESTAMP(gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) % 3600) / 60), ' m'
                           )
                   END as duration
            FROM (
                SELECT vehicle_number, trip_id, timestamp, gate_entry_number, gate_entry_in_time,
                       loading_or_unloading, green_channel, gate_exit_status, gate_entry_status,
                       MAX(CASE WHEN location = 'GATE EXIT' THEN time END) 
                           OVER (PARTITION BY trip_id) as gate_exit_time,
                       ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY timestamp) as rn
                FROM document_summary_view_dummy
                WHERE DATE(timestamp) = :today_date
            ) sub
            WHERE rn = 1
        """
        
        # Gate In query
        gate_in_base = base_query + " AND gate_entry_number IS NOT NULL"
        
        # Gate Out query
        gate_out_base = base_query + " AND gate_entry_status = 'Close'"
        
        # Gate Dock Pending query
        gate_dock_pending_base = """
            SELECT dsv.vehicle_number, dsv.trip_id, dsv.timestamp, dsv.gate_entry_number, dsv.gate_entry_in_time,
                   dsv.loading_or_unloading, dsv.green_channel, dsv.gate_exit_status, dsv.gate_entry_status,
                   dsv.gate_exit_time,
                   CASE 
                       WHEN dsv.gate_exit_status = 'EXITED' AND dsv.gate_exit_time IS NOT NULL THEN 
                           CONCAT(
                               FLOOR(EXTRACT(EPOCH FROM (dsv.gate_exit_time - TO_TIMESTAMP(dsv.gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) / 3600), ' h ',
                               FLOOR((EXTRACT(EPOCH FROM (dsv.gate_exit_time - TO_TIMESTAMP(dsv.gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) % 3600) / 60), ' m'
                           )
                       ELSE 
                           CONCAT(
                               FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - TO_TIMESTAMP(dsv.gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) / 3600), ' h ',
                               FLOOR((EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - TO_TIMESTAMP(dsv.gate_entry_in_time, 'DD-MON-YYYY HH24:MI:SS'))) % 3600) / 60), ' m'
                           )
                   END as duration
            FROM (
                SELECT vehicle_number, trip_id, timestamp, gate_entry_number, gate_entry_in_time,
                       loading_or_unloading, green_channel, gate_exit_status, gate_entry_status,
                       MAX(CASE WHEN location = 'GATE EXIT' THEN time END) 
                           OVER (PARTITION BY trip_id) as gate_exit_time,
                       ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY timestamp) as rn
                FROM document_summary_view_dummy
                WHERE DATE(timestamp) = :today_date
                  AND gate_entry_number IS NOT NULL
            ) dsv
            LEFT JOIN dock_summary_view dkv ON dsv.trip_id = dkv.trip_id
            WHERE dsv.rn = 1 AND dkv.trip_id IS NULL
        """

        columns = ["vehicle_number", "trip_id", "timestamp", "gate_entry_number", "gate_entry_in_time",
                   "loading_or_unloading", "green_channel", "gate_exit_status", "gate_entry_status",
                   "gate_exit_time", "duration"]

        # Detail responses
        if card_type == "gate_in":
            query = apply_load_type_filter(gate_in_base, load_type) + " ORDER BY timestamp ASC"
            result = db.session.execute(text(query), {"today_date": today}).fetchall()
            data = [list(row) for row in result]
            return jsonify({"success": True, "columns": columns, "data": data}), 200

        elif card_type == "gate_out":
            query = apply_load_type_filter(gate_out_base, load_type) + " ORDER BY timestamp ASC"
            result = db.session.execute(text(query), {"today_date": today}).fetchall()
            data = [list(row) for row in result]
            return jsonify({"success": True, "columns": columns, "data": data}), 200

        elif card_type == "gate_dock_pending":
            query = apply_load_type_filter(gate_dock_pending_base, load_type) + " ORDER BY timestamp ASC"
            result = db.session.execute(text(query), {"today_date": today}).fetchall()
            data = [list(row) for row in result]
            return jsonify({"success": True, "columns": columns, "data": data}), 200

        # Summary counts (unchanged)
        def get_count(base_sql, load_type_val=None):
            sql = base_sql
            if load_type_val in ('loading', 'unloading'):
                sql = apply_load_type_filter(sql, load_type_val)
            result = db.session.execute(text(sql), {"today_date": today}).fetchall()
            return len(result)

        gate_in_loading = get_count(gate_in_base, "loading")
        gate_in_unloading = get_count(gate_in_base, "unloading")
        gate_out_loading = get_count(gate_out_base, "loading")
        gate_out_unloading = get_count(gate_out_base, "unloading")
        gate_dock_pending_loading = get_count(gate_dock_pending_base, "loading")
        gate_dock_pending_unloading = get_count(gate_dock_pending_base, "unloading")

        return jsonify({
            "success": True,
            "counts": {
                "gate_in": {
                    "loading": gate_in_loading,
                    "unloading": gate_in_unloading,
                    "total": gate_in_loading + gate_in_unloading
                },
                "gate_out": {
                    "loading": gate_out_loading,
                    "unloading": gate_out_unloading,
                    "total": gate_out_loading + gate_out_unloading
                },
                "gate_dock_pending": {
                    "loading": gate_dock_pending_loading,
                    "unloading": gate_dock_pending_unloading,
                    "total": gate_dock_pending_loading + gate_dock_pending_unloading
                }
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# # ===================== DOCK API =====================
# @app.route("/api/dock", methods=["GET"])
# def dock_api():
#     try:
#         today = date.today()
#         card_type = request.args.get("type")

#         location_map = {
#             "lmhp": "LMHP", "hhp": "HHP", "genset": "Genset",
#             "rmstore": "RM Store", "rwh": "RWH", "estore": "EStore", "other": "Other"
#         }

#         columns = ["vehicle_number", "trip_id", "transporter_name", "loading_unloading",
#                    "docked_location", "dock_location_invoice", "start_time", "end_time", "docked_duration"]

#         # Return detail data if a specific card type is requested
#         if card_type in location_map:
#             loc = location_map[card_type]
#             query = text("""
#                 SELECT vehicle_number, trip_id, transporter_name, loading_unloading,
#                        docked_location, dock_location_invoice, start_time, end_time, docked_duration
#                 FROM dock_summary_view
#                 WHERE DATE(start_time) = :today_date AND docked_location = :loc AND end_time IS NULL
#             """)
#             result = db.session.execute(query, {"today_date": today, "loc": loc}).fetchall()
#             data = [list(row) for row in result]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         # Summary counts for all dock locations
#         counts = {}
#         for key, loc in location_map.items():
#             query = text("""
#                 SELECT COUNT(*) FROM dock_summary_view
#                 WHERE DATE(start_time) = :today_date AND docked_location = :loc AND end_time IS NULL
#             """)
#             cnt = db.session.execute(query, {"today_date": today, "loc": loc}).scalar() or 0
#             counts[key] = cnt

#         return jsonify({"success": True, "counts": counts}), 200

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500


# # ===================== DOCK API =====================
# @app.route("/api/dock", methods=["GET"])
# def dock_api():
#     try:
#         today = date.today()
#         card_type = request.args.get("type")
#         load_type = request.args.get("load_type")  # 'loading', 'unloading', or None

#         location_map = {
#             "lmhp": "LMHP", "hhp": "HHP", "genset": "Genset",
#             "rmstore": "RM Store", "rwh": "RWH", "estore": "EStore", "other": "Other"
#         }

#         columns = ["vehicle_number", "trip_id","gate_entry_number", "transporter_name", "loading_unloading",
#                    "docked_location", "dock_location_invoice", "start_time", "end_time", "docked_duration"]

#         # Return detail data if a specific card type is requested
#         if card_type in location_map:
#             loc = location_map[card_type]
#             # Base query: currently docked (end_time IS NULL) and at the specified location
#             query = """
#                 SELECT vehicle_number, trip_id, gate_entry_number,transporter_name, loading_unloading,
#                        docked_location, dock_location_invoice, start_time, end_time, docked_duration
#                 FROM dock_summary_view
#                 WHERE DATE(start_time) = :today_date 
#                   AND docked_location = :loc 
#                   AND end_time IS NULL
#                   ORDER BY start_time ASC
#             """
#             # Apply load_type filter if provided
#             if load_type in ('loading', 'unloading'):
#                 # query += " AND loading_unloading = :load_type_val"
#                 query = """
#                 SELECT vehicle_number, trip_id, gate_entry_number,transporter_name, loading_unloading,
#                        docked_location, dock_location_invoice, start_time, end_time, docked_duration
#                 FROM dock_summary_view
#                 WHERE DATE(start_time) = :today_date 
#                   AND docked_location = :loc 
#                   AND end_time IS NULL
#                   AND loading_unloading = :load_type_val
#                 ORDER BY start_time ASC
#                 """

#                 result = db.session.execute(
#                     text(query), 
#                     {"today_date": today, "loc": loc, "load_type_val": load_type.capitalize()}
#                 )
#             else:
#                 result = db.session.execute(text(query), {"today_date": today, "loc": loc})
            
#             data = [list(row) for row in result.fetchall()]
#             return jsonify({"success": True, "columns": columns, "data": data}), 200

#         # --- Summary counts for all locations (split by loading/unloading) ---
#         counts = {}
#         for key, loc in location_map.items():
#             # Count loading (currently docked, end_time IS NULL, loading_unloading = 'Loading')
#             query_loading = text("""
#                 SELECT COUNT(*) FROM dock_summary_view
#                 WHERE DATE(start_time) = :today_date 
#                   AND docked_location = :loc 
#                   AND end_time IS NULL
#                   AND loading_unloading = 'Loading'
#             """)
#             loading_cnt = db.session.execute(query_loading, {"today_date": today, "loc": loc}).scalar() or 0

#             # Count unloading
#             query_unloading = text("""
#                 SELECT COUNT(*) FROM dock_summary_view
#                 WHERE DATE(start_time) = :today_date 
#                   AND docked_location = :loc 
#                   AND end_time IS NULL
#                   AND loading_unloading = 'Unloading'
#             """)
#             unloading_cnt = db.session.execute(query_unloading, {"today_date": today, "loc": loc}).scalar() or 0

#             counts[key] = {
#                 "loading": loading_cnt,
#                 "unloading": unloading_cnt,
#                 "total": loading_cnt + unloading_cnt
#             }

#         return jsonify({"success": True, "counts": counts}), 200

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500
                
# ===================== DOCK API =====================
@app.route("/api/dock", methods=["GET"])
def dock_api():
    try:
        today = date.today()
        card_type = request.args.get("type")
        load_type = request.args.get("load_type")  # 'loading', 'unloading', or None

        location_map = {
            "lmhp": "LMHP", "hhp": "HHP", "genset": "Genset",
            "rmstore": "RM Store", "rwh": "RWH", "estore": "EStore", "other": "Other"
        }

        columns = ["vehicle_number", "trip_id","gate_entry_number", "transporter_name", "loading_unloading",
                   "docked_location", "dock_location_invoice", "start_time", "end_time", "docked_duration", "current_duration"]

        # Return detail data if a specific card type is requested
        if card_type in location_map:
            loc = location_map[card_type]
            # Base query: currently docked (end_time IS NULL) and at the specified location
            query = """
                SELECT vehicle_number, trip_id, gate_entry_number, transporter_name, loading_unloading,
                       docked_location, dock_location_invoice, start_time, end_time, docked_duration,
                       CONCAT(
                           FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - start_time)) / 3600), ' h ',
                           FLOOR((EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - start_time)) % 3600) / 60), ' m'
                       ) as current_duration
                FROM dock_summary_view
                WHERE DATE(start_time) = :today_date 
                  AND docked_location = :loc 
                  AND end_time IS NULL
                  ORDER BY start_time ASC
            """
            # Apply load_type filter if provided
            if load_type in ('loading', 'unloading'):
                query = """
                    SELECT vehicle_number, trip_id, gate_entry_number, transporter_name, loading_unloading,
                           docked_location, dock_location_invoice, start_time, end_time, docked_duration,
                           CONCAT(
                               FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - start_time)) / 3600), ' h ',
                               FLOOR((EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - start_time)) % 3600) / 60), ' m'
                           ) as current_duration
                    FROM dock_summary_view
                    WHERE DATE(start_time) = :today_date 
                      AND docked_location = :loc 
                      AND end_time IS NULL
                      AND loading_unloading = :load_type_val
                    ORDER BY start_time ASC
                """
                result = db.session.execute(
                    text(query), 
                    {"today_date": today, "loc": loc, "load_type_val": load_type.capitalize()}
                )
            else:
                result = db.session.execute(text(query), {"today_date": today, "loc": loc})
            
            data = [list(row) for row in result.fetchall()]
            return jsonify({"success": True, "columns": columns, "data": data}), 200

        # --- Summary counts for all locations (split by loading/unloading) ---
        counts = {}
        for key, loc in location_map.items():
            # Count loading (currently docked, end_time IS NULL, loading_unloading = 'Loading')
            query_loading = text("""
                SELECT COUNT(*) FROM dock_summary_view
                WHERE DATE(start_time) = :today_date 
                  AND docked_location = :loc 
                  AND end_time IS NULL
                  AND loading_unloading = 'Loading'
            """)
            loading_cnt = db.session.execute(query_loading, {"today_date": today, "loc": loc}).scalar() or 0

            # Count unloading
            query_unloading = text("""
                SELECT COUNT(*) FROM dock_summary_view
                WHERE DATE(start_time) = :today_date 
                  AND docked_location = :loc 
                  AND end_time IS NULL
                  AND loading_unloading = 'Unloading'
            """)
            unloading_cnt = db.session.execute(query_unloading, {"today_date": today, "loc": loc}).scalar() or 0

            counts[key] = {
                "loading": loading_cnt,
                "unloading": unloading_cnt,
                "total": loading_cnt + unloading_cnt
            }

        return jsonify({"success": True, "counts": counts}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# ------------------------------------------------------------
# Run Flask App
# ------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(
        host="0.0.0.0",
        port=5400,
        debug=True,
        ssl_context=("kirloskarWC2025.crt", "kirloskarWC2025.key")
    )
