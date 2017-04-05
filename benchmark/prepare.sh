#! /bin/sh

set  -x

mysqlhost='127.0.0.1'
mysqlport='630'
user='root'
pass='test.,1'
db='dbtest'
tablecount=10
tablesize=50000
interval=10
disttype='uniform'
randinit='on'
maxrequest=0
testmod='nontrx'
nontrxmod='select'
areadonly='on'
skiptrx='on'
maxtime=120
threads=120



for a in `seq 1 4`

do
        echo "$a""test"
        echo "$mysqlport""$a"
        #echo "start ss call"
        #ss -it dst "$serverip"  >> $log_file
        #echo $(date +"%Y-%m-%d %H:%M:%S") >> $log_file

        sleep 1
        /usr/local/sysbench-0.5/bin/sysbench --test=/usr/local/sysbench-0.5/share/tests/db/oltp.lua \
        --mysql-host="$mysqlhost" --mysql-port="$mysqlport""$a" --mysql-user="$user" --mysql-password="$pass" \
        --mysql-db=$db --oltp-tables-count=$tablecount --oltp-table-size=$tablesize \
        --report-interval=$interval --oltp-dist-type="$disttype" --rand-init="$randinit" --max-requests=$maxrequest \
        --oltp-test-mode="$testmod" --oltp-nontrx-mode="$nontrxmod" \
        --oltp-read-only="$areadonly" --oltp-skip-trx="$skiptrx" \
        --max-time=$maxtime --num-threads=$threads prepare \

done

