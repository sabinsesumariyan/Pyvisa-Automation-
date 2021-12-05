clc
clear 
close all
%%frequency count value
file=fopen('E:\KTU\Sem3\Electronic measurement system\Lab1_attempt2\ExpData\Frequency_count.txt','r');
frequency_count=fscanf(file,'%d\n');
fclose(file);
frequency_count=frequency_count-1;
%%
Frequency_array = zeros(1,frequency_count);
file=fopen('E:\KTU\Sem3\Electronic measurement system\Lab1_attempt2\ExpData\frequency_list.txt','r');
readvalue=fscanf(file,'%d\n');
count=1;
fclose(file);
for i=readvalue(1):readvalue(2):readvalue(3)
    Frequency_array(count)=i;
    count=count+1;
end
%%
file=fopen('E:\KTU\Sem3\Electronic measurement system\Lab1_attempt2\ExpData\Scopevar.txt','r');
Scope_var=fscanf(file,'%f\n');
Sampling_frequency=Scope_var(1);
Sample_length=Scope_var(2);
fclose(file);
%%
input_array = zeros(1,frequency_count);
output_array=zeros(1,frequency_count);
time=(0:(Sample_length-1))/Sampling_frequency;
Transmission_1 = zeros(1,frequency_count);
Transmission_2 = zeros(1,frequency_count);
Transmission_3 = zeros(1,frequency_count);
vref=(0.01/32);
offset=0;%Time offset
for i=1:1:frequency_count
    N = int2str(i);
    Data=strcat('E:\KTU\Sem3\Electronic measurement system\Lab1_attempt2\ExpData\Scope_data_a',N);
    load(Data); 
    in=(double(ch1)-127)*vref-offset;
    out=(double(ch2)-127)*vref-offset;
    Uest_in = SWCtruncated(time,2*pi*Frequency_array(i),in);
    Uest_out = SWCtruncated(time,2*pi*Frequency_array(i),out);
    Transmission_1(i)=Uest_out/Uest_in;
end
vref=(0.1/32);
for i=1:1:frequency_count
    N = int2str(i);
    Data=strcat('E:\KTU\Sem3\Electronic measurement system\Lab1_attempt2\ExpData\Scope_data_b',N);
    load(Data); 
    in=(double(ch1)-127)*vref-offset;
    out=(double(ch2)-127)*vref-offset;
    Uest_in = SWCtruncated(time,2*pi*Frequency_array(i),in);
    Uest_out = SWCtruncated(time,2*pi*Frequency_array(i),out);
    Transmission_2(i)=Uest_out/Uest_in;
    
end
vref=(1/32);
for i=1:1:frequency_count
    N = int2str(i);
    Data=strcat('E:\KTU\Sem3\Electronic measurement system\Lab1_attempt2\ExpData\Scope_data_c',N);
    load(Data); 
    in=(double(ch1)-127)*vref-offset;
    out=(double(ch2)-127)*vref-offset;
    Uest_in = SWCtruncated(time,2*pi*Frequency_array(i),in);
    Uest_out = SWCtruncated(time,2*pi*Frequency_array(i),out);
    Transmission_3(i)=Uest_out/Uest_in;
end
%%
figure(1)
plot(Frequency_array/1e6,10*log(10)*(abs(Transmission_1)),'r');
hold on
plot(Frequency_array/1e6,10*log(10)*(abs(Transmission_2)),'g');
hold on
plot(Frequency_array/1e6,10*log(10)*(abs(Transmission_3)),'b');
xt = [2 2 2];
yt = [20 31 12];
str = {'Gain 2 ','Gain 3','Gain 1'};
text(xt,yt,str)
title("Magnitude Plot ");
xlabel('Frequency (MHz)');
ylabel('Magnitude (dB)');
grid on;



figure(2)
plot(Frequency_array/1e6,angle(Transmission_1),'r');
hold on
plot(Frequency_array/1e6,angle(Transmission_2),'g');
hold on
plot(Frequency_array/1e6,angle(Transmission_3),'b');
xt = [0.2 4.3 3.5];
yt = [2 2.2 1];
str = {'Gain 2 ','Gain 3','Gain 1'};
text(xt,yt,str)
title("Phase Plot");
xlabel('Frequency (MHz)');
ylabel('Phase angle (Rad)');
grid on;

%%






