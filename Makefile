all: server sync callback coroutine

server: server.py
	python server.py&

sync: sync.py
	python sync.py

callback: async_cb.py
	python async_cb.py

coroutine: async_coroutine.py
	python async_coroutine.py
