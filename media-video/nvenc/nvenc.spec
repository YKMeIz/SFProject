Name:           nvenc
Version:        5.0.1
Release:        1%{?dist}
Summary:        Hardware-Accelerated H.264 and HEVC (H.265) Video Encoding

License:        https://developer.nvidia.com/nvidia-video-codec-sdk-license-agreement
URL:            https://developer.nvidia.com/nvidia-video-codec-sdk
Source0:        http://developer.download.nvidia.com/compute/%{name}/v5.0/%{name}_%{version}_sdk.zip

BuildArch:      noarch

%description
The NVIDIA Encoder (NVENC) API enables software developers to access the
high-performance hardware H.264 and HEVC (H.265) video encoder in Kepler and
Maxwell class NVIDIA GPUs. NVENC provides high-quality video encoding that is
faster and more power efficient in comparison to equivalent CUDA-based or
CPU-based encoders. By using dedicated hardware for the video encoding task, the
GPU CUDA cores and/or the CPU are available for other compute-intensive tasks.
NVENC on GeForce hardware can support a maximum of 2 concurrent streams per
system. NVENC for GRID, Tesla and certain Quadro GPUs (see below) can support as
many streams as possible up to maximum NVENC encoder rate limit and available
video memory.

%package samples
Summary:        nvEncoder Sample application source code
Requires:       %{name} = %{version}-%{release}

%description samples
This package contains nvEncoder Sample application source code demonstrating
various encoding capabilities.

%prep
%setup -q -n %{name}_%{version}_sdk

%install
install -m 644 -p -D Samples/common/inc/nvEncodeAPI.h \
    %{buildroot}%{_includedir}/%{name}/nvEncodeAPI.h
ln -sf %{_includedir}/%{name}/nvEncodeAPI.h Samples/common/inc/nvEncodeAPI.h

%files
%doc doc/NVENC_VideoEncoder_API_ProgGuide.pdf doc/NvEncodeAPI_v.5.0.pdf
%{_includedir}/%{name}

%files samples
%doc Release_notes.txt ReadMe.txt Samples doc/NVENC_DA-06209-001_v06.pdf

%changelog
* Fri Apr 10 2015 Simone Caronni <negativo17@gmail.com>
- First build.
