# ansible-personal



| File			| Task			| Tags					| Comments |
|---			|---			|---					|--- |
| root.sh		| root.yml		| skip: view_new,update	| Выполняется из под root на этапе установки |
| main.sh		| main.yml		| skip: view_new,update	| Выполняется из под локального пользователя для настройки машины |
| hass.sh	    | -				| -						| Создание образов и установка на rpi HomeAssistant |
| view_new.sh	| main.yml		| tags: view_new,init	| ? |
| update.sh		| main.yml		| tags: update,init		| ? |
| test.sh		| main.yml		| tags: test,init		| Для отладки скриптов |
| archsrv.sh	| archsrv.yml	|						| ? |
