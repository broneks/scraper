import json

def write_to_file(output):
    with open(f'./output/blog-posts-content-final.json', 'w') as file:
        json.dump(output, file, indent=2, ensure_ascii=False)

def filter_out_empty(json):
    output = {
        'blog_posts': [],
    }

    output['blog_posts'] = list(filter(lambda p: len(p['paragraphs']) > 0, json['blog_posts']))

    return output

def main():
    try:
        f = open('./output/blog-posts-content.json')
    except:
        print('blog content file does not exist.')

    blog_content_json = json.load(f)
    filtered_blog_content_json = filter_out_empty(blog_content_json)

    write_to_file(filtered_blog_content_json)

main()
