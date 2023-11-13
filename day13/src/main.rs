use std::{env, str::Chars};

enum ListItem {
    Num(u32),
    SubList(Vec<ListItem>),
}

fn place_at_depth_rec(depth: u32, tree: &mut Vec<ListItem>, item: u32) {
    let mut end_list = match tree.last().unwrap() {
        ListItem::Num(_) => panic!(),
        ListItem::SubList(li) => li,
    };

    if depth == 1 {
        end_list.push(ListItem::Num(item));
    } else {
        place_at_depth_rec(depth - 1, &mut end_list, item);
    }
}

fn main() {
    let mut pairs: Vec<(&str, &str)> = Vec::new();
    let mut list_pairs: Vec<(Vec<ListItem>, Vec<ListItem>)> = Vec::new();

    let binding: String = env::args().nth(1).unwrap();
    binding.split("\n\n").for_each(|two_lines: &str| {
        let mut x = two_lines.split("\n");
        pairs.push((x.clone().nth(0).unwrap(), x.nth(1).unwrap()));
    });

    pairs.iter().for_each(|p| {
        println!("{} {}", p.0, p.1);
    });

    // Build lists
    pairs.iter().for_each(|pair| {
        let mut lhs_found_first = false;
        let mut rhs_found_first = false;

        let mut lhs: Vec<ListItem> = Vec::new();
        let mut rhs: Vec<ListItem> = Vec::new();

        let mut lhs_curr_depth = 0;
        pair.0.chars().skip(1).for_each(|c| match c {
            '[' => {
                lhs.push(ListItem::SubList(Vec::new()));
                lhs_curr_depth += 1;
            }
            ']' => {
                lhs_curr_depth -= 1;
            }
            ',' => print!("Comma"),
            num => {
                if lhs_curr_depth == 0 {
                    lhs.push(ListItem::Num(num.to_digit(10).unwrap()))
                } else {
                    let mut new_depth = lhs_curr_depth.clone();
                    let mut curr_vec: &Vec<ListItem> = &lhs;
                    while new_depth > 0 {}
                }
            }
        })
    });
}
