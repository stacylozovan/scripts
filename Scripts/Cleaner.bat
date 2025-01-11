rem Установка кодовой страницы UTF-8
chcp 65001

rem Удаление папок
rem ----

for /d %%f in ("4OTO" "Android" "Movies" "Music" "Pictures" "Download" "Notifications" "Podcasts" "Recordings" "Ringtones" ) do (
  echo Удаление папки "%%f"...
  rmdir "%%f" /s /q
)

rem ----

echo **Готово!**

pause