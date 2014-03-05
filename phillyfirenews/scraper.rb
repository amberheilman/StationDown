require 'pry'
require 'nokogiri'
require 'open-uri'
require 'awesome_print'
require 'fileutils'
require 'csv'

class PhillyFireNewsParser
  def url(page = 1)
    "http://www.phillyfirenews.com/category/fire_wire/pennsylvania/city-of-philadelphia/feed/?paged=#{page}"
  end

  def get(url_path)
    begin
      open(url_path)
    rescue OpenURI::HTTPError => error
      nil
    end
  end

  def parse_page(page = 1)
    text    = get(url(page))
    unless text.nil?
      xml     = Nokogiri::XML(text)
      stories = xml.xpath('//channel/item/content:encoded').map do |node|
        parse_html(node.inner_html)
      end
      return stories
    else
      nil
    end
  end

  def line_type(line)
    if line =~ /Date/
      return :date
    end

    if line =~ /Time/
      return :time
    end

    if line =~ /Town/
      return :town
    end

    if line =~ /Address/
      return :address
    end

    if line =~ /Type/
      return :type
    end

    if line =~ /Details/
      return :details
    end

    if line =~ /The post/
      return :link
    end

    return :unknown
  end

  def data_from(line)
    br_regex   = Regexp.new("<br \/>")
    type_regex = Regexp.new("Date:|Time:|Town:|Address:|Type:")
    html       = line.split("</strong>", 2).last.gsub(br_regex, "").strip rescue ""

    begin
      Nokogiri::HTML(html).xpath("//text()").remove.first.text.gsub(type_regex, "").strip
    rescue => error
      nil
    end
  end

  def extract(line)
    [line_type(line), data_from(line)]
  end

  def parse_html(html)
    hash = {}
    html.split("\n").map do |line|
      type, data = extract(line)
      hash[type] = data
    end
    hash
  end

  def all_pages_to_csv!
    i      = 1
    p      = PhillyFireNewsParser.new
    result = p.parse_page(i)

    FileUtils.rm("philly_fire_news.csv") if File.exists?("philly_fire_news.csv")
    FileUtils.touch("philly_fire_news.csv")

    CSV.open("philly_fire_news.csv", "w+") do |csv|
      csv << ["date", "time", "town", "address", "type"]
      until result.nil?
        result.each do |row|
          csv << [row[:date], row[:time], row[:town], row[:address], row[:type]]
        end
        result = p.parse_page(i)
        i += 1
      end
    end
  end
end

# ap result
