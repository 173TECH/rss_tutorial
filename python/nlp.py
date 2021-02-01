import pandas as pd
from .misc.processing import desc_text
from datetime import datetime
from sayn import PythonTask


class LanguageProcessing(PythonTask):

    def run(self):

        # Assign the required parameters

        table = self.parameters["user_prefix"] + self.task_parameters["table"]
        text_fields = self.parameters["text"]


        # Read from database to dataframe

        df = pd.DataFrame(self.default_db.read_data(f"SELECT * FROM {table}"))

        # Process the texts from article titles and summaries

        for t in text_fields:
            self.info(f"Processing texts for {t} field")
            desc_text(df, t, "english")
            self.info("Processing Completed!")

        # Load the processed texts back into the database

        df.published = df.published.apply(lambda x: datetime.strptime(x, '%a, %d %b %Y %H:%M:%S %Z')) # Convert published timestamps to datetime

        if df is not None:
            output = f"{table}_{self.name}"
            n_rows = len(df)
            self.info(f"Loading {n_rows} rows into destination: {output}....")
            df.to_sql( output,
                       self.default_db.engine,
                       if_exists="replace",
                       index=False)
            self.info("Load done.")


        return self.success()
