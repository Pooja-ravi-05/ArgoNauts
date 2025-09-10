from sqlalchemy import create_engine

def load_to_postgres(df, db_url="postgresql://postgres:your_password@localhost:5432/floatchat"):
    # Rename "time" to avoid PostgreSQL reserved keyword
    df = df.rename(columns={"time": "measurement_time"})
    
    engine = create_engine(db_url)
    
    df.to_sql('argo_data', engine, if_exists='append', index=False)
    
    print("Data loaded successfully into PostgreSQL!")

