string = "\\r\\n_SHOT;0;1;1000;60;3;15:50:38.60;3;1;32;10;103;0;2;0.00000000;0.00520000;900;0;0;655.35;745155015;65535;0;0\\r\\n_TOTL;0;1;1000;103;T;0-0*;0;Q;0;0;S;0;0;\\r\\n'"
string.replace("\\\\r\\\\n", "")
string.replace("\"", "")
string.replace("\'", "")
lst = string.split(";")
print(lst)