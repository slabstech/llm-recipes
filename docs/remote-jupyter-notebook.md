Access Jupyter notebook from remote server

- On Remote server
    - Create python  virtual environment
        - python -m venv venv
    - Enable virtual environment
        - source -m venv venv
    - Install Jupyter notebook
        - pip install notebook
    - Enable security for jupyter server
        - jupyter server password
            - Enter new password
    -  Start notebook 
        - jupyter notebook --no-browser --port=8888

- On Local Machine
    - ssh -L 8888:localhost:8888 remote-user@remote-server

    - vistit localhost:8888 on the broweser