
.PHONY = run

RUNNING_APP = "ps -A | grep streamlit | cut -d " " -f1"

run:
	@cd src/streamlit_app && export STREAMLIT_SERVER_PORT=5000 && streamlit run app.py &
kill:
	@echo ${RUNNING_APP}
	@kill -KILL ${RUNNING_APP}
