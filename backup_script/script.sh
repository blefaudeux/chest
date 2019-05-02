#!/usr/bin/env sh

BACKUP_COMMAND='duplicacy backup --threads 6'
CLEANUP_COMMAND='duplicacy prune -keep 15:7'
BACKUP_CONFIG=$HOME/.backup/
TMP_MAIL=$BACKUP_CONFIG/tmp_mail
TMP_LOG=$BACKUP_CONFIG/tmp_backup.log
LOG=$BACKUP_CONFIG/backup.log

log()
{
    echo $1
    echo $1 >> $2
}

backup_folder()
{
    folder=$1
    cwd=`pwd`
    folder_name=`basename ${folder}`
    cd $1

    # Echo the ongoing work, save in the log also
    log "\nBacking up $folder" $TMP_LOG
    pwd

    # Mark this folder as WIP
    SEMAPHORE="$BACKUP_CONFIG/$folder_name.log"
    echo "WIP" > $SEMAPHORE
    date >> $TMP_LOG
    cd $folder
    $BACKUP_COMMAND >> $TMP_LOG
    $CLEANUP_COMMAND >> $TMP_LOG
    cd $cwd
    rm  $SEMAPHORE
}

backup_path()
{
    echo "Looking for backups under $1"

    for folder in `find $1 -name "*.duplicacy*" -type d`
    do
        folder_path=${folder%/.duplicacy}
        backup_folder $folder_path
    done
}

send_success_mail()
{
    echo "To:$1\n" > $TMP_MAIL
    echo "From:lefaudeux.backup@gmail.com\n" >> $TMP_MAIL
    echo "Subject: Backup was successful\n\n" >> $TMP_MAIL
    echo " *** Everything is fine ! **"  >> $TMP_MAIL
    echo " - Log : \n" >> $TMP_MAIL
    cat $TMP_LOG >> $TMP_MAIL
    mail $1 < $TMP_MAIL
    rm $TMP_MAIL
}

# Run the backup
echo "\n\n *** New backup session *** \n" > $TMP_LOG
sleep 5

backup_path $HOME
backup_path "/media/Data"
echo "Backup done"

# Post-backup maintenance
# - send mail with the log
send_success_mail 'benjamin.lefaudeux@gmail.com'

# - save the global log onsite
cat $TMP_LOG >> $LOG
rm $TMP_LOG
