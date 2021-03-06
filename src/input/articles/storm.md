title: Крупнейший суперкомпьютер оказался в руках злоумышленников
date: 2007-09-04
labels: articles
author: umonkey
source: http://web.archive.org/web/20071119010041/deadchannel.ru/story/2451
---
Крупнейший в истории человечества [суперкомпьютер][super] был запущен в конце
августа, однако это событие оказалось [практически незамеченным][noatt] широкой
общественностью.

[Ботнет][botnet] «[Storm][]», состоящий из инфицированных троянами компьютеров,
на данный момент по разным оценкам насчитывает от одного до десяти миллионов
систем (до этого крупнейшим СК был [BlueGene/L][], состоящий из 128,000
процессорных систем).  Средняя частота процессора в Шторме — 2.5ГГц, объём
памяти — 1Гб, скоростью доступа к сети — около 2Мб/сек
([подробности][details]).  Его производительность превосходит суммарную
производительность десяти мощнейших СК, [известных до этого момента][known].

В отличие от всех остальных СК, подконтрольных правительственным структурам,
«Шторм», по всем внешним признакам, является творением злоумышленников, однако
их конечные цели пока неизвестны.  Объединение [троянов][trojan] и
[червей][worm] в сети,
манипулируемые злоумышленником — обыденное явление; обычно такие сети
используются для рассылки спама или хулиганства (можно, например, «завалить» на
время какой-нибудь сервер).  Такую сеть легко вывести из строя, нарушив её связь
с центральным, координирующим сервером, превратив отдельные машины в безвредных
зомби; эти сервера в течении нескольких часов вычисляются и обезвреживаются
лабораториями по разработке антивирусов.  В случае с «Штормом» такой сценарий не
сработает, по двум причинам.

Во-первых, анализ существующего кода показывает, что в данном случае
центрального сервера нет: сеть остроена по принципу «[peer-to-peer][]», каждая
заражённая машина поддерживает контакт с нескольким десятком других машин, но
полный их список отсутствует (именно это затрудняет точную оценку размеров
сети).  Машины могут взаимодействовать друг с другом, команды извне сети они не
принимают.  Отключить их можно только разобравшись в протоколе общения и, как
это ни парадоксально, поразив сеть другим, «исцеляющим» вирусом.  Если, конечно,
протокол общения это допускает.

Во-вторых, в «Шторм» заложен инстинкт самосохранения.  Он постоянно следит за
безопасностью заражённых систем и, при обнаружении сканирования или попытки
проникновения в них, сам запускает скоординированную атаку на сеть, из которой
производится вторжение.  В силу описанной распределённой структуры сети, атака
сначала может показаться не очень сильной, но она способна раскачаться до
колоссальных объёмов.

Кроме того, с момента обнаружения несколько раз менялся способ распространения:
сначала использовалась почтовая рассылка исполняемых файлов, затем —
распространение ссылок на заражённые файлы, открываемые браузером, затем —
завлечение пользователей на сайт, внешне очень похожий на YouTube.  Причины и
источники этих мутаций неизвестны.  Скорее всего, модицфикация была произведена
авторами червя, но при такой производительности и правильных начальных
алгоритмах, полученному суперкомпьютеру вполне по силам «читать» новости о себе
в Google News, новости о дырах в системах безопасности, менять тактику,
параллельно лишая известные антивирусные лаборатории интернета.

Всё это уже сейчас выходит за рамки простых шуток школьников и студентов, и не
исключено, что в конечном счёте источником «Шторма» окажется вовсе не простой
злоумышленник, и даже не антивирусная лаборатория.  Шутки ради вспомним
[описание SkyNet][SkyNet] по версии авторов «Терминатора 3»:

> Skynet was created as a United States Air Force project, a distributed
> computer network designed to create new military vehicles and make strategic
> decisions as well as protect their computer systems from virus attacks.  One
> such virus had infected their defense computers, crippling them all.  Under
> pressure, the Air Force attempted to use Skynet to remove the virus, not
> realizing that Skynet was sentient and had created the virus in order to
> manipulate humanity into giving it control over the world's computers.  Skynet
> was initially thought to be capable of being shut down if only someone could
> reach its system core, but ultimately it was discovered that it was nothing
> more than software that ran by spreading throughout the world's computer
> networks and had no central point from which it could be disabled.

Одно можно сказать точно: при любом исходе этот прецедент сильно повлияет на
компьютерные вирусы будущего.  Их авторы редко отличаются изобретательностью, но
любят воспроизводить (постепенно оттачивая) известные им технологии.  Активная
самооборона — новое слово в вирусостроении, остаётся всего один шаг:
самообучение.

## Обновление от 09.09.2007

Очередная спам-атака «Шторма» призывает пользователя установить клиент «Tor» —
систему анонимизации, делающую невозможным отслеживание трафика пользователя. 
Сам «Шторм» не использует Tor для своих целей, побочный эффект такого
паразитирования — огромное внимание к системе, официально призванной обезопасить
людей от вторжения в личную жизнь.  Технологии корпораций фактически
используются для борьбы с «большим братом», или, по крайней мере, нас заставляют
так думать.

Что касается самого «Шторма», для понижения собственной уязвимости он применяет
набирающую популярность технологию [fast-flux DNS][], использующую огромное
количество резервных дублирующих серверов, динамически перераспределяющих
обязанности.  В случае со «Штормом», количество таких серверов составляет
примерно 2000, распределены они по четырём сотням провайдеров в 50 странах мира.
Это — количество серверов, которое необходимо отключить, чтобы вывести «Шторм»
из строя.

> «Fast-flux — это не плохие парни, пытающиеся спрятаться.  Это — плохие парни,
> которые говорят: мы здесь, приди и забери нас.  И ты не можешь.» — Эдам
> Уотерс, начальник службы поддержки Security Intelligence.

Спасиры использовали fast-flux ещё в конце 90-х, когда большая часть
пользователей интернета использовала dial-up.  Уже тогда отключить их было
крайне сложно, единственный способ — удалить запись о регистрации домена из
глобального DNS.  Но когда ботнеты используют свой собственный DNS, не имеющий
отношения к тому, который контроллирует американская организация ICANN,
отключить их практически невозможно.  По оценкам компании «Secure Computing»,
занимающейся сетевой безопасностью, общий объём ботнетов, на данный момент
использующих технологию fast-flux, составляет примерно 50 миллионов машин.

[BlueGene/L]: http://en.wikipedia.org/wiki/Blue_Gene
[SkyNet]: http://en.wikipedia.org/wiki/Skynet_%28fictional%29
[Storm]: http://en.wikipedia.org/wiki/Storm_Worm
[botnet]: http://ru.wikipedia.org/wiki/%D0%91%D0%BE%D1%82%D0%BD%D0%B5%D1%82
[details]: http://www.steampowered.com/status/survey.html
[fast-flux DNS]: http://www.securityfocus.com/news/11473
[known]: http://www.top500.org/
[noatt]: http://seclists.org/fulldisclosure/2007/Aug/0520.html
[peer-to-peer]: http://ru.wikipedia.org/wiki/%D0%9E%D0%B4%D0%BD%D0%BE%D1%80%D0%B0%D0%BD%D0%B3%D0%BE%D0%B2%D0%B0%D1%8F_%D1%81%D0%B5%D1%82%D1%8C
[super]: http://ru.wikipedia.org/wiki/%D0%A1%D1%83%D0%BF%D0%B5%D1%80%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80
[trojan]: http://ru.wikipedia.org/wiki/%D0%A2%D1%80%D0%BE%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B5_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B
[worm]: http://ru.wikipedia.org/wiki/%D0%A1%D0%B5%D1%82%D0%B5%D0%B2%D1%8B%D0%B5_%D1%87%D0%B5%D1%80%D0%B2%D0%B8
