from pyspark.sql import SparkSession

path = "mydata.csv"

spark = SparkSession.builder.appName('Out').getOrCreate()
df = spark.read.csv(path)
df=spark.read.option('header', 'true').csv(path)
# df.select('Name').show()
# df.describe().show()
# df.withColumn("Age after 2", df['Age']+2) ( Adding New Col )
# df.na.drop()
# df.na.drop(subset=['Age']) ( drop None value in age )
# df.na.drop(thresh=2) ( drop row have min 2 None value )
# df.na.fill('***',subset=['Age','City'])
# df.filter("Age<40")
# df.filter(~(df['age']<=40)) ( Not Op )

df = df.groupBy('city').sum()
print(df.show())