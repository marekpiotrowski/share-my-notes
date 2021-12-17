from sqlalchemy import create_engine, text

if __name__ == "__main__":
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())
    print("Hello, world!")
