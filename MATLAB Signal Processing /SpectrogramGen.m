%Spectrogram Generator Code
%Author: Dichochi Ramotlou
%Date: 15 July 2024
function [S,f,t]= SpectrogramGen(y,fs,N,overlap)

y = single(y(:)).';  %Convert y to a sngle row vector 
ylen = length(y);    
window = taylorwin(N,4,-30).'; 
Overlap_NumSamples = floor(overlap*N); %Compute the overlap samples from overlap factor
hop = N - Overlap_NumSamples; 
numFrames = floor((ylen - N) / (hop))+1;
S = [];% Spectrogram Matrix
for i = 1:numFrames
    % Start and end indices for the current frame
    startIdx = (i-1) * (N - Overlap_NumSamples ) +1;
    endIdx = startIdx + N - 1;
    
    frame = y(startIdx:endIdx);
    windowedFrame= frame .*window;
    frameFFT = fftshift(fft(windowedFrame));               
    
   % Store the magnitude of the FFT result
   S(:, end + 1) = abs(frameFFT); 

end
t = (N/2:hop:N/2+(numFrames-1)*hop)/fs;     % Time (s)
f = (-N/2:1:(N/2-1))*fs/N;     %Frequency  (Hz)
end



