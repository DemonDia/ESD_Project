FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./AccRejCMS.py ./userDecisionCMS.py ./ApplyJobCMS.py ./CreateJobCMS.py ./
COPY ./ownerStatusSMS.py ./userStatusSMS.py ./ApplicationSMS.py ./UserSMS.py ./jobSMS.py ./
COPY ./main.py ./invokes.py ./
COPY ./direct_amqp_setup.py ./ownerNoti_AMQP.py ./ErrorSMS.py ./ownerNotificationSMS.py ./userNoti_AMQP.py ./topic_amqp_setup.py ./
CMD [ "python", "./AccRejCMS.py" ]
