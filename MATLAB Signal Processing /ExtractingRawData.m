
function [S]= ExtractingRawData()

% Open the file for reading
fileID = fopen("IQRunning.txt", 'r');
ADC_bits = 12;
ADC_intervals = 2^ADC_bits;
% Initialize an empty array to store the numbers
ComplexVectorArray =[];
i=0;
while ~feof(fileID) && i<=199%Only take 40 000 samples(200X200) 
    i=i+1;
    % Get the next line from the file
    line = fgetl(fileID);
    
    % Split the line into space-separated numbers
    numbers = str2double(strsplit(line));
    

      I= numbers(1:200);
      Q= numbers(201:400);

I = I * (1 / ADC_intervals) - 2048 * (1 / ADC_intervals);
Q = Q * (1 / ADC_intervals) - 2048 * (1 / ADC_intervals);

% Create the complex vector
ComplexVector = I + 1i * Q;
ComplexVectorArray = [ComplexVectorArray, ComplexVector];
end
S=ComplexVectorArray ;