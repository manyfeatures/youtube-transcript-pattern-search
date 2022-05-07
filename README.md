# Description
Script to scan all videos in YouTube channel and find patterns in transcripts

### How to use
- Add firefox driver for selenium
- Specify the channel
- create pattern to search 


###### Example
```
channel_videos_url = "https://www.youtube.com/c/MadHighlights/videos"
web_driver_path = "./geckodriver"
pattern = "\s(\w+)?(флан|flan)(\w*)?"
```

some results
```
Scanning video | Мэддисон играет в Макса Пейна НА РУЛЕ | https://www.youtube.com/watch?v=4CsK9a-2Y38


===================================================
2:09#дома max payne который похож на дом фландерс на мой взгляд то это уже будет

21:31#пока не хочу о дом flanders малый совет по нему приятно

===================================================


Scanning video | Мэддисон играет в Lost Ark и прощается с Твичем | https://www.youtube.com/watch?v=wWTp4TkPF2s


===================================================
10:57#серию симпсон нет нет нет нигде дом flanders а где они в китай приехали и

15:38#этого показали огромный гигантский корабль который заходил уже в мирный отбитый порт и на нем стоял над фландерс

16:15#проходил до этого моменты надо flanders там не было такого добавили сегодня в патч 35 мегабайт качался апдейт

57:09#ну фландрский пустой сам с любовью

===================================================
```
