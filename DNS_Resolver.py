# Patrick Wszeborowski
# CSE 310
# SBU ID: 111007547
# Spring 2021
# Assignment 1

# Part A

import dns.query
import re
import time
from datetime import datetime
# This function is used for the initial query sent to one of the root servers,
# hard-coded here as 198.41.0.4.

# If it doesn't find an answer initially, parameters are sent to the recursive function,
# namely, the query message object and the first IP address found in the additional section
def initial_recursive_resolver(query_msg):
    # makes the first response message and sends it using TCP to 198.41.0.4
    dns_start = time.perf_counter()
    now = datetime.now()
    response_msg = dns.query.tcp(query_msg, '198.41.0.4')
    response_msg_to_text = response_msg.to_text()
    # gets the index value of "ANSWER"
    answer_val = response_msg_to_text.find('ANSWER')
    answer_text_lines = response_msg_to_text[answer_val:].split("\n")
    answer_line = answer_text_lines[1]
    # BONUS: resolving the cname if it's in ANSWER
    cname_match = re.search("CNAME", answer_line)
    if cname_match is not None:
        answer_line_frags = answer_line.split(" ")
        if answer_line_frags[3] == "CNAME":
            # we stop the performance timer
            dns_end = time.perf_counter()
            # and we list the information
            print("ANSWER SECTION:")
            print(answer_line)
            print("Query time:", (dns_end - dns_start),"s")
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("WHEN:", dt_string)
            return
    # this is a regular expression denoting the match of an IP address
    ip_address_regex = r"((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}"
    # makes a match object to see if a line matches an IP address
    match = re.search(ip_address_regex, answer_line)
    # if the ANSWER section provides the resolved IP address
    if match is not None:
        # we stop the performance timer
        dns_end = time.perf_counter()
        # and we list the information
        print("ANSWER SECTION:")
        print(answer_line)
        print("Query time:", (dns_end - dns_start),"s")
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        print("WHEN:", dt_string)
        return
    # if ANSWER is not found, then we go to ADDITIONAL
    # gets the index value of "ADDITIONAL"
    additional_val = response_msg_to_text.find("ADDITIONAL")
    # finds the message of what ADDITIONAL provides from the received query response
    additional_text_lines = response_msg_to_text[additional_val:].split("\n")
    for line in additional_text_lines:
        words = line.split(" ")
        for word in words:
            # tries to find if there is a valid IP address under ADDITIONAL
            # and sends it as a parameter to the recursive function
            match = re.search(ip_address_regex, word)
            if match is not None:
                recursive_resolver(query_msg, match.group(), now, dns_start)
                return

# The recursive function used after the initial function has passed its parameters here
# goes through the first valid IP address it finds in the ADDITIONAL section,
# and when it eventually finds a valid CNAME or ANSWER IP address, prints the results
def recursive_resolver(query_msg, ip_address, now, dns_start):
    response_msg = dns.query.tcp(query_msg, ip_address)
    response_msg_to_text = response_msg.to_text()
    # gets the index value of "ANSWER"
    answer_val = response_msg_to_text.find('ANSWER')
    answer_text_lines = response_msg_to_text[answer_val:].split("\n")
    answer_line = answer_text_lines[1]
    # BONUS: resolving the cname
    cname_match = re.search("CNAME", answer_line)
    if cname_match is not None:
        answer_line_frags = answer_line.split(" ")
        if answer_line_frags[3] == "CNAME":
            query_msg = dns.message.make_query(answer_line_frags[4][:-1], 'A')
            response_msg = dns.query.tcp(query_msg, '198.41.0.4')
            response_msg_to_text = response_msg.to_text()
            # gets the index value of "ANSWER"
            answer_val = response_msg_to_text.find('ANSWER')
            answer_text_lines = response_msg_to_text[answer_val:].split("\n")
            answer_line = answer_text_lines[1]

            # this is a regular expression denoting the match of an IP address
            ip_address_regex = r"((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}"
            # makes a match object to see if a line matches an IP address
            match = re.search(ip_address_regex, answer_line)
            # if the ANSWER section provides the resolved IP address
            if match is not None:
                # we stop the performance timer
                dns_end = time.perf_counter()
                # and we list the information
                print("ANSWER SECTION:")
                print(answer_line)
                print("Query time:", (dns_end - dns_start),"s")
                dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
                print("WHEN:", dt_string)
                return
            # if ANSWER is not found, then we go to ADDITIONAL
            # gets the index value of "ADDITIONAL"
            additional_val = response_msg_to_text.find('ADDITIONAL')
            additional_text_lines = response_msg_to_text[additional_val:].split("\n")
            for line in additional_text_lines:
                words = line.split(" ")
                for word in words:
                    match = re.search(ip_address_regex, word)
                    if match is not None:
                        recursive_resolver(query_msg, match.group(), now, dns_start)
                        return

    # this is a regular expression denoting the match of an IP address
    ip_address_regex = r"((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}"
    # makes a match object to see if a line matches an IP address
    match = re.search(ip_address_regex, answer_line)
    # if the ANSWER section provides the resolved IP address
    if match is not None:
        # we stop the performance timer
        dns_end = time.perf_counter()
        # and we list the information
        print("ANSWER SECTION:")
        print(answer_line)
        print("Query time:", (dns_end - dns_start),"s")
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        print("WHEN:", dt_string)
        return
    # if ANSWER is not found, then we go to ADDITIONAL
    # gets the index value of "ADDITIONAL"
    additional_val = response_msg_to_text.find('ADDITIONAL')
    additional_text_lines = response_msg_to_text[additional_val:].split("\n")
    for line in additional_text_lines:
        words = line.split(" ")
        for word in words:
            match = re.search(ip_address_regex, word)
            if match is not None:
                recursive_resolver(query_msg, match.group(), now, dns_start)
                return

    # to resolve NS records in the event of one, i.e. for amazon.com
    answer_line = answer_text_lines[2]
    answer_line_frags = answer_line.split(" ")
    if answer_line_frags[3] == "NS":
        query_msg = dns.message.make_query(answer_line_frags[4][:-1], 'A')
        response_msg = dns.query.tcp(query_msg, '198.41.0.4')
        response_msg_to_text = response_msg.to_text()
        # gets the index value of "ANSWER"
        answer_val = response_msg_to_text.find('ANSWER')
        answer_text_lines = response_msg_to_text[answer_val:].split("\n")
        answer_line = answer_text_lines[1]
        # makes a match object to see if a line matches an IP address
        match = re.search(ip_address_regex, answer_line)
        # if the ANSWER section provides the resolved IP address
        if match is not None:
            # we stop the performance timer
            dns_end = time.perf_counter()
            # and we list the information
            print("ANSWER SECTION:")
            print(answer_line)
            print("Query time:", (dns_end - dns_start),"s")
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("WHEN:", dt_string)
            return
        # if ANSWER is not found, then we go to ADDITIONAL
        # gets the index value of "ADDITIONAL"
        additional_val = response_msg_to_text.find('ADDITIONAL')
        additional_text_lines = response_msg_to_text[additional_val:].split("\n")
        for line in additional_text_lines:
            words = line.split(" ")
            for word in words:
                match = re.search(ip_address_regex, word)
                if match is not None:
                    recursive_resolver(query_msg, match.group(), now, dns_start)
                    return

domain_name = input("Enter a domain name: ")
query_msg = dns.message.make_query(domain_name, 'A')
print("QUESTION SECTION:")
print(domain_name, "\t\t IN A")
initial_recursive_resolver(query_msg)
