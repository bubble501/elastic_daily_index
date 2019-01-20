# elastic_daily_index
elastic_daily_index will help you rollover the index daily and delete the old index according your configurations. the default value is keeping index newer than 14 days. you can change the value of self.age according your requirement.

## quick start
1. clone the local disk, we assume the default base directory is /opt
```
git clone https://github.com/bubble501/elastic_daily_index.git
```
2. install the required package.
```
pip3 install -r requirements.txt
```
3. create the needed index template, alias and index using the following script.
```
python daily_index.py demo --action create
```
4. edit the rollover.sh based on your index name.
5. Add the follow line to your cron job using crontab -e.
```
00 1 * * * /opt/elastic_daily_index/rollover.sh
```
6. Now you can use index alias demo_write as the index name of your index writer and index alias demo_search as the index name of your index reader.
