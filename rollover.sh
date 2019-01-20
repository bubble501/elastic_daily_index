# assume that the base directory of elastic_daily_index is /opt
# add to the crontab like this:
# 00 1 * * * /opt/elastic_daily_index/rollover.sh > /tmp/roll_over.log

now=`date`
echo "$now start rollover blocks..." 
 python /opt/elastic_daily_index/daily_index.py  demo --action rollover
 
sleep 30
now=`date`
echo "$now start delete_old transactions..."
python /opt/elastic_daily_index/daily_index.py demo --action delete_old

