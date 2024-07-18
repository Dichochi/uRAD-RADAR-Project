
% Input parameters
CPI = 0.25; % seconds

% Constants
c = 299792458; % (m/s) speed of light
fc = 24e9; % (Hz) Center frequency 
maxSpeed_km_hr = 4/1000*(60*60); % (km/hr) maximum speed to display
minSpeed_km_hr = 0.4/1000*(60*60); % (km/hr) maximum speed to display
Time_MinimumtoDiplay_s = 0; 

% computations
lamda = c/fc;



% Compute the spectrogram 
fs=1e3;
NumSamplesPerFrame =  2^(nextpow2(round(CPI*fs)));      % Ensure its a power of 2
OverlapFactor = 0.8;                                    % Overlap factor between successive frames 
Y= ExtractingRawData();
[S, f, t] = SpectrogramGen(Y,fs, NumSamplesPerFrame, OverlapFactor);

speed_m_per_sec = f*lamda/2;
speed_km_per_hr = speed_m_per_sec*(60*60/1000);
speed_km_per_hr_Idx = find((speed_km_per_hr <= maxSpeed_km_hr) & (speed_km_per_hr >= minSpeed_km_hr));

SpeedVectorOfInterest_km_hr = speed_km_per_hr(speed_km_per_hr_Idx);
SpeedVectorOfInterest_m_s = SpeedVectorOfInterest_km_hr*1000/60/60;

t_idx = find((t <= t(end)) & (t >= Time_MinimumtoDiplay_s));
t_OfInterest_s = t(t_idx);

S_OfInterest = S(speed_km_per_hr_Idx, t_idx);

S_OfInterestToPlot = abs(S_OfInterest)/max(max(abs(S_OfInterest)));

% Plot the spectrogram - km/hr
clims = [-50 0];
figure; imagesc(t_OfInterest_s,SpeedVectorOfInterest_km_hr,20*log10(S_OfInterestToPlot), clims);
xlabel('Time (s)');
ylabel('Speed (km/hr)');
grid on;
colorbar;
colormap('jet');
axis xy;

% Plot the spectrogram - m/s
clims = [-50 0];
figure; imagesc(t_OfInterest_s,SpeedVectorOfInterest_m_s,20*log10(S_OfInterestToPlot), clims);
xlabel('Time (s)');
ylabel('Speed (m/s)');
grid on;
colorbar;
colormap('jet');
axis xy;

 




