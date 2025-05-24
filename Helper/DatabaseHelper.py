import pyodbc
import asyncio

class DatabeHelper:
    CONNECTION_STRING = (
        "DRIVER={SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=DEVELOPMENT;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    @staticmethod
    async def get_profile():
        profile = {}
        try:
            loop = asyncio.get_running_loop()
            connection = await loop.run_in_executor(None,pyodbc.connect,DatabeHelper.CONNECTION_STRING)
            cursor = connection.cursor()
            query = "SELECT * FROM SystemProfile WHERE Profile = 'PythonLLMAPI'"
            cursor.execute(query)

            row = cursor.fetchone()
            if row:
                columns = [column[0] for column in cursor.description]
                profile = dict(zip(columns, row))

            cursor.close()
            connection.close()

        except Exception as ex:
            print(f"Error retrieving PythonLLMAPI profile from database: {ex}")

        return profile



