all: build

build:
	@echo "ОТКЛЮЧЕНО. Сборка не работает ввиду остутствия модуля poolemonkey."
	@#python ./poole.py --build --ignore '^\.|~$$|\.ccss$$' # --base-url=http://www.deadchannel.ru

update: build
	-git --work-tree=output --git-dir=output/.git add .
	-git --work-tree=output --git-dir=output/.git commit -am "Web site udpdate."
	-git --work-tree=output --git-dir=output/.git push
	-git add .
	-git commit -am "Web site udpdate."
	-git push

serve:
	PYTHONPATH=$(PWD) poole.py --serve
