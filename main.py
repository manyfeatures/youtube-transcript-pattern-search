# Search of words time steps in video/videos transcripts from the given YouTube channel
from WebDriver import *
import os
from pathlib import Path

def find_pattern(channel_vidos_url, pattern, file):
    with open(os.path.join(channel_vidos_url, file), 'r') as f:
        lines = f.readlines()
    all_matches = []
    for line in lines:
        res = [x.group(0) for x in re.finditer(pattern, line)]
        #if res: all_matches.append(res)
        if res: all_matches.append(line)
    return all_matches

def find_pattern_in_files(channel_vidos_url, pattern):
    df = pd.read_csv(os.path.join(channel_vidos_url, 'videos_metadata.csv'), sep=';')
    print('Searching pattern in all videos')
    with open(os.path.join(channel_vidos_url, 'results.txt'), 'a+') as f:
        for _, row in tqdm(df.iterrows()):
            # print results
            print('\033[1;36;48m' + f'Scanning video | {row.title} | {row.link}' + '\033[1;37;0m')
            print('\n')
            print('===================================================')
            res = find_pattern(channel_vidos_url, pattern, row.file)
            print(*res, sep='\n')
            print('===================================================')
            print('\n')

            # save to file
            f.write('\n\n\n'+'=================================================')
            f.write(f'|Video: {row.title} {row.link} {row.file}|\n')
            f.write('\n'.join(res))

def main():
    channel_videos_url = "https://www.youtube.com/c/MadHighlights/videos"
    web_driver_path = "./geckodriver"
    #driver = WebDriver(channel_videos_url, web_driver_path)
    ## send --headless to prevent browser opening

    #driver.open_page()
    #driver.scroll_to_end()
    #driver.get_all_content()
    #driver.save_videos_transcripts()
    #driver.exit() # make it context manager?
    #del driver

    pattern = "\s(\w+)?(флан|flan)(\w*)?"
    metadata_path = Path(channel_videos_url).parent.stem
    find_pattern_in_files(metadata_path, pattern)

if __name__ == "__main__":
    main()