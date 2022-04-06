# **CSE5911 - AllocVote (previously ENOVA)**

## First Iteration Contributers
* Amjad Rammahi
* Zhiren Xu
* Collin Wright
* Luke Howard
* Tian Liang - Original Contributer
* Jennifer Heider - Original Contributer

## Second Iteration Contributers
* Brian Dong
* Sarah Zhang
* Liam Gallagher
* Christopher Tuttle

## Project Overview

[Efficient Near-Optimal Voting Allocation.PDF](Efficient&#32;Near-Optimal&#32;Voting&#32;Allocation.pdf)

# Resources

### *[Determining resource requirements for elections using indifference-zone generalized binary search](https://www.sciencedirect.com/science/article/pii/S0360835219307120)*

ScienceDirect paper, covers IZGBS.

# Notes
* Initial runtime of the code was 1622.43 seconds (benchmarked on OSC).

* Apportionment assumes an infinite number of resources (voting machines, check-in booths, etc.) per location. The goal of apportionment is to return the mininum number of resources that meet a specified wait time requirement (no more than 30 minutes, no more than 60 minutes, etc.).
* Allocation takes in a fixed number of resources with a fixed number of locations. The goal of allocation is to calculate how best to distribute resources to minimize total wait times. Allocation will use apportionment in its calculation.

# Setup
We recommend working on this project in Visual Studio Code, as it was the original IDE this program was developed on.

1. Download VSCode
2. Clone this github repository
3. Optional: Install the WSL (Windows Subsystem for Linux) if working on a Windows environment
4. Install Python + Python Extension for VSCode
5. Install pip with
```
sudo apt install python3-pip
```
6. Install required packages with 
```
pip install -r requirements.txt
```
7. Optional: If the files are not installed on PATH, copy the file path in which they are installed in to PATH

# Usage

To run apportionment:
```
python3 apportionment.py voting_excel.xlsm
```
To run allocation:
```
python3 apportionment.py voting_excel.xlsm
```
Use "--log critical" to only print critical logs
```
python3 apportionment.py voting_excel.xlsm --log critical
```

# Changing Program Settings
All settings for both allocation and apportionment are controlled from the Settings page within the voting_excel.xlsm file. Any settings changed and saved on this page will be effective on the next run of the software.
